#!/usr/bin/env python3
"""Audit content/ for markdown files that cannot be indexed as timeline events.

Orphans = .md under content/ that do not match XX.YY.ZZ-slug.md (content_events / build-events).
Exits with code 1 if any orphans are found.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from build_events_from_content import discover_content_files  # noqa: E402


def main():
    files, orphans = discover_content_files()
    if orphans:
        print(f"Audit failed: {len(orphans)} content file(s) not indexable as events:\n")
        for p in orphans:
            print(f"  - {p}")
        print("\nRename to XX.YY.ZZ-slug.md (or remove) so Relay content_events can index them.")
        sys.exit(1)

    print(f"Audit passed: all {len(files)} content files match XX.YY.ZZ-slug.md")
    sys.exit(0)


if __name__ == "__main__":
    main()
