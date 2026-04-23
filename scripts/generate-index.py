#!/usr/bin/env python3
"""Generate index.json file tree for paradigm-threat-timeline. Used by file browser, not by timeline component."""
import os
import json
import subprocess
from datetime import datetime, timezone
from typing import Dict, Optional

# Minified JSON (smaller index for fetch). Images keep _width/_height only.
_JSON_DUMP_KW = {"separators": (",", ":"), "ensure_ascii": False}


def _git_last_commit_unix_times(repo_dir: str) -> Dict[str, int]:
    """Newest-first `git log`; first sighting of each path = last commit touching it."""
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                repo_dir,
                "log",
                "--no-renames",
                "--name-only",
                "--pretty=format:%ct",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return {}

    last: Dict[str, int] = {}
    current_ts: Optional[int] = None
    for line in proc.stdout.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.isdigit():
            current_ts = int(s)
            continue
        if current_ts is None:
            continue
        key = s.replace("\\", "/")
        if key not in last:
            last[key] = current_ts
    return last


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

    git_times = _git_last_commit_unix_times(repo_dir)

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
                        try:
                            from PIL import Image
                            with Image.open(full_path) as img:
                                file_data["_width"], file_data["_height"] = img.size
                        except Exception:
                            pass

                    rel_posix = os.path.relpath(full_path, repo_dir).replace("\\", "/")
                    ts = git_times.get(rel_posix)
                    if ts is not None:
                        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                        file_data["_updated"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    else:
                        try:
                            mtime = os.path.getmtime(full_path)
                            dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
                            file_data["_updated"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                        except OSError:
                            pass

                    tree[item] = file_data
                    total_files += 1

        return tree, total_files

    tree, count = build_tree(repo_dir)
    tree['_count'] = count

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tree, f, **_JSON_DUMP_KW)

    print(f"Generated index.json with {count} files at {output_file}")

if __name__ == "__main__":
    generate_index()
