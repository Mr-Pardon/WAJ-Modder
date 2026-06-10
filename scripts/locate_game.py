#!/usr/bin/env python3
"""Locate Witch's Apocalyptic Journey and its WorkshopUploader."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


GAME_DIR_NAME = "Witch's Apocalyptic Journey"
EXE_NAME = "Witch's Apocalyptic Journey.exe"
UPLOADER_REL = Path("Witch's Apocalyptic Journey_Data") / "StreamingAssets" / "Mod Upload Tool" / "WorkshopUploader.exe"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-dir", help="Known game install directory")
    parser.add_argument("--steam-dir", default=r"C:\Program Files (x86)\Steam", help="Steam install directory")
    return parser.parse_args()


def steam_libraries(steam_dir: Path) -> list[Path]:
    libraries = [steam_dir]
    vdf = steam_dir / "steamapps" / "libraryfolders.vdf"
    if not vdf.is_file():
        return libraries
    text = vdf.read_text(encoding="utf-8", errors="ignore")
    for match in re.finditer(r'"path"\s+"([^"]+)"', text):
        libraries.append(Path(match.group(1).replace("\\\\", "\\")))
    return list(dict.fromkeys(libraries))


def candidates(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    if args.game_dir:
        paths.append(Path(args.game_dir))
    steam_dir = Path(args.steam_dir)
    for lib in steam_libraries(steam_dir):
        paths.append(lib / "steamapps" / "common" / GAME_DIR_NAME)
    return list(dict.fromkeys(paths))


def validate_game_dir(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "exists": path.is_dir(),
        "exe": str(path / EXE_NAME),
        "exe_exists": (path / EXE_NAME).is_file(),
        "data_dir_exists": (path / "Witch's Apocalyptic Journey_Data").is_dir(),
        "uploader": str(path / UPLOADER_REL),
        "uploader_exists": (path / UPLOADER_REL).is_file(),
    }


def main() -> int:
    args = parse_args()
    results = [validate_game_dir(path) for path in candidates(args)]
    found = [item for item in results if item["exists"] and item["data_dir_exists"]]
    print(json.dumps({"found": found, "checked": results}, ensure_ascii=False, indent=2))
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
