#!/usr/bin/env python3
"""Find or clone the official Witch's Apocalyptic Journey mod tutorial repo."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_REPO = "https://github.com/meowalive/apocalyptic-journey-mod-tutorial.git"
KNOWN_NAMES = ["mod-tutorial", "apocalyptic-journey-mod-tutorial"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Workspace/root directory to search or clone into")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--dest", help="Destination folder name or path; default is mod-tutorial under root")
    parser.add_argument("--no-clone", action="store_true", help="Only search; do not clone if missing")
    return parser.parse_args()


def is_tutorial(path: Path) -> bool:
    return (path / "ModTemplate" / "ModConfig.json").is_file()


def find_tutorial(root: Path) -> Path | None:
    roots = [root, *root.parents]
    for base in roots:
        for name in KNOWN_NAMES:
            candidate = base / name
            if is_tutorial(candidate):
                return candidate
    for candidate in root.rglob("ModTemplate"):
        parent = candidate.parent
        if is_tutorial(parent):
            return parent
    return None


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    found = find_tutorial(root)
    if found:
        print(found)
        return 0
    if args.no_clone:
        print("Tutorial repo not found.", file=sys.stderr)
        return 1
    dest = Path(args.dest).resolve() if args.dest else root / "mod-tutorial"
    if dest.exists():
        print(f"Destination exists but is not a valid tutorial repo: {dest}", file=sys.stderr)
        return 2
    subprocess.run(["git", "clone", "--depth", "1", args.repo, str(dest)], check=True)
    if not is_tutorial(dest):
        print(f"Clone completed but ModTemplate was not found: {dest}", file=sys.stderr)
        return 1
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
