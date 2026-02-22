#!/usr/bin/env python3
"""Generate a styled PDF from all content/*.md files -> public/timeline.pdf"""
import os, re, base64, glob, mimetypes, sys, io

try:
    import markdown as md_lib
except ImportError:
    print("ERROR: pip install markdown", file=sys.stderr); sys.exit(1)
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("ERROR: pip install weasyprint", file=sys.stderr); sys.exit(1)
try:
    from PIL import Image
except ImportError:
    print("ERROR: pip install Pillow", file=sys.stderr); sys.exit(1)

# Max image width in pixels for PDF (1200px ≈ 170mm at 180 DPI – plenty for A4)
MAX_IMAGE_WIDTH = 1200
JPEG_QUALITY = 72

import json as _json

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_DIR    = os.path.dirname(SCRIPT_DIR)
CONTENT_DIR = os.path.join(REPO_DIR, "content")
PUBLIC_DIR  = os.path.join(REPO_DIR, "public")
OUTPUT_PDF  = os.path.join(PUBLIC_DIR, "timeline.pdf")
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Read version from package.json
with open(os.path.join(REPO_DIR, "package.json"), "r") as _f:
    PKG_VERSION = _json.load(_f)["version"]

CSS_STYLES = """
/* No remote font imports - use system fonts only to avoid network hangs */
@page {
    size: A4;
    margin: 22mm 20mm 25mm 20mm;
    @bottom-left {
        content: 'v""" + PKG_VERSION + """';
        font-family: sans-serif;
        font-size: 8pt;
        color: #aaa;
    }
    @bottom-center {
        content: counter(page);
        font-family: sans-serif;
        font-size: 9pt;
        color: #888;
    }
}
* { box-sizing: border-box; }
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
    background: #fff;
    margin: 0; padding: 0;
}
.article { page-break-before: always; }
.article:first-child { page-break-before: avoid; }
h1 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 22pt; font-weight: 700; color: #111;
    margin: 0 0 0.6em 0; padding-bottom: 0.3em;
    border-bottom: 2.5px solid #b8860b; line-height: 1.2;
}
h2 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 15pt; font-weight: 700; color: #2c2c2c;
    margin: 1.4em 0 0.5em 0; border-bottom: 1px solid #ddd; padding-bottom: 0.2em;
}
h3 {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12pt; font-weight: 700; color: #3a3a3a;
    margin: 1.2em 0 0.4em 0;
}
p { margin: 0 0 0.9em 0; orphans: 3; widows: 3; }
a { color: #8b6914; text-decoration: none; }
.img-wrap {
    text-align: center; margin: 1.4em 0; page-break-inside: avoid;
}
.img-wrap img {
    max-width: 100%; max-height: 240px; height: auto;
    border-radius: 3px; box-shadow: 0 1px 6px rgba(0,0,0,0.18);
}
.img-wrap .caption {
    display: block; font-size: 8.5pt; color: #666;
    font-style: italic; margin-top: 0.4em; line-height: 1.4;
}
blockquote {
    margin: 1em 0; padding: 0.6em 1.2em;
    border-left: 4px solid #b8860b; background: #fdf8ee;
    color: #333; font-style: italic; page-break-inside: avoid;
}
blockquote p { margin: 0; }
code {
    font-family: 'Courier New', monospace; font-size: 9pt;
    background: #f5f5f5; padding: 1px 4px; border-radius: 2px;
}
pre {
    background: #f5f5f5; padding: 0.8em 1em;
    border-radius: 4px; font-size: 8.5pt; page-break-inside: avoid;
}
pre code { background: none; padding: 0; }
ul, ol { margin: 0.5em 0 0.9em 0; padding-left: 1.8em; }
li { margin-bottom: 0.3em; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em 0; }
.section-label {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 8pt; letter-spacing: 0.12em;
    text-transform: uppercase; color: #999; margin-bottom: 0.3em;
}
"""

def embed_image(src):
    """Resize, compress, and base64-encode an image for PDF embedding."""
    rel = src.lstrip("/")
    abs_path = os.path.join(REPO_DIR, rel)
    if not os.path.isfile(abs_path):
        return src
    try:
        img = Image.open(abs_path)
        # Resize if wider than MAX_IMAGE_WIDTH
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            new_h = int(img.height * ratio)
            img = img.resize((MAX_IMAGE_WIDTH, new_h), Image.LANCZOS)
        # Convert to RGB for JPEG output (handles RGBA PNGs)
        if img.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/jpeg;base64,{data}"
    except Exception as e:
        print(f"    WARNING: Could not process image {rel}: {e}", file=sys.stderr)
        # Fallback: embed raw file
        mime, _ = mimetypes.guess_type(abs_path)
        if not mime: mime = "image/jpeg"
        try:
            with open(abs_path, "rb") as fh:
                return f"data:{mime};base64,{base64.b64encode(fh.read()).decode('ascii')}"
        except OSError:
            return src

def strip_jsx(text):
    return re.sub(r"<[A-Z][A-Za-z0-9]*/?>", "", text)

def md_to_html(text):
    exts = ["markdown.extensions.tables","markdown.extensions.fenced_code",
            "markdown.extensions.nl2br","markdown.extensions.sane_lists",
            "markdown.extensions.smarty"]
    return md_lib.markdown(text, extensions=exts)

def process_images(html):
    def replace_src(m):
        src = m.group(1)
        return m.group(0).replace(src, embed_image(src))
    html = re.sub(r'<img\s[^>]*src="([^"]+)"', replace_src, html)
    def wrap_img(m):
        img_tag = m.group(1); caption_em = m.group(2) or ""
        alt_m = re.search(r'alt="([^"]*)"', img_tag)
        alt = alt_m.group(1) if alt_m else ""
        ct = re.sub(r"</?em>","",caption_em).strip() if caption_em else alt
        ch = f'<span class="caption">{ct}</span>' if ct else ""
        return f'<div class="img-wrap">{img_tag}{ch}</div>'
    html = re.sub(r"<p>(<img\b[^>]+>)\s*(?:<br\s*/?>)?\s*(<em>[^<]*</em>)?\s*</p>", wrap_img, html, flags=re.DOTALL)
    return html

def get_section(fn):
    m = re.match(r"(\d+\.\d+)", os.path.basename(fn))
    return m.group(1) if m else ""

def build_article(path, first):
    with open(path,"r",encoding="utf-8") as f: text = f.read()
    text = strip_jsx(text)
    html = process_images(md_to_html(text))
    sn = get_section(path)
    lbl = f'<p class="section-label">{sn}</p>' if sn else ""
    pb = "" if first else 'style="page-break-before:always"'
    return f'<article class="article" {pb}>{lbl}{html}</article>\n'

def main():
    md_files = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")))
    if not md_files:
        print("No markdown files in content/", file=sys.stderr); sys.exit(1)
    print(f"Found {len(md_files)} content files")
    articles = ""
    for i, p in enumerate(md_files):
        print(f"  Processing {os.path.basename(p)}")
        articles += build_article(p, first=(i==0))
    full = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Paradigm Threat Timeline</title></head><body data-version="{PKG_VERSION}">{articles}</body></html>"""
    fc = FontConfiguration()
    css = CSS(string=CSS_STYLES, font_config=fc)
    print(f"Rendering PDF -> {OUTPUT_PDF}")
    HTML(string=full, base_url=REPO_DIR).write_pdf(OUTPUT_PDF, stylesheets=[css], font_config=fc)
    mb = os.path.getsize(OUTPUT_PDF) / (1024*1024)
    print(f"Done. {mb:.1f} MB -> {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
