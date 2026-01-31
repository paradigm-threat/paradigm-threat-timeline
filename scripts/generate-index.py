#!/usr/bin/env python3
"""Generate index.json file tree for paradigm-threat-timeline. Used by file browser, not by timeline component."""
import os
import json

def get_lqip(image_path):
    """Generates a 16x16 base64-encoded WebP LQIP string for an image. Returns None if PIL unavailable."""
    try:
        from PIL import Image
        import base64
        import io
        with Image.open(image_path) as img:
            img.thumbnail((16, 16))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", quality=20)
            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/webp;base64,{base64_str}"
    except Exception:
        return None

def generate_index():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    output_file = os.path.join(repo_dir, "index.json")

    exclude_dirs = {'.git', '.github', 'scripts', 'node_modules', '.idea'}
    exclude_files = {
        'index.json',
        'package-lock.json',
        'package.json',
        '.gitignore',
    }

    include_exts = {'.md', '.txt', '.pdf', '.json', '.jpg', '.jpeg', '.png', '.webp'}

    def build_tree(current_path):
        tree = {}
        total_files = 0

        try:
            items = os.listdir(current_path)
        except PermissionError:
            return {}, 0

        for item in sorted(items):
            if item in exclude_files or item.startswith('.'):
                continue

            full_path = os.path.join(current_path, item)

            if os.path.isdir(full_path):
                if item in exclude_dirs:
                    continue
                subtree, count = build_tree(full_path)
                tree[item] = subtree
                tree[item]['_count'] = count
                total_files += count
            else:
                ext = os.path.splitext(item)[1].lower()
                if ext in include_exts:
                    title = None
                    if ext == '.md':
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                for _ in range(20):
                                    line = f.readline()
                                    if not line:
                                        break
                                    line = line.strip()
                                    if line.startswith('# '):
                                        title = line[2:].strip()
                                        break
                                    if line.startswith('title:'):
                                        title = line[6:].strip().strip('"').strip("'")
                                        break
                        except Exception:
                            pass

                    file_data = {}
                    if title:
                        file_data["_title"] = title

                    if ext in {'.jpg', '.jpeg', '.png', '.webp'}:
                        lqip = get_lqip(full_path)
                        if lqip:
                            file_data["_lqip"] = lqip

                    tree[item] = file_data
                    total_files += 1

        return tree, total_files

    tree, count = build_tree(repo_dir)
    tree['_count'] = count

    with open(output_file, 'w') as f:
        json.dump(tree, f, indent=2)

    print(f"Generated index.json with {count} files at {output_file}")

if __name__ == "__main__":
    generate_index()
