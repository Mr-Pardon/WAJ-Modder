#!/usr/bin/env python3
"""Create a Witch's Apocalyptic Journey Lua mod draft from ModTemplate."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


KNOWN_TUTORIAL_NAMES = ["mod-tutorial", "apocalyptic-journey-mod-tutorial"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", help="Path to mod-tutorial/ModTemplate")
    parser.add_argument("--out", required=True, help="Directory where the mod folder will be created")
    parser.add_argument("--name", required=True, help="ModName and output folder name")
    parser.add_argument("--author", default="Unknown")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--description", default="A Witch's Apocalyptic Journey Lua mod draft.")
    parser.add_argument("--visibility", default="Private", choices=["Private", "FriendsOnly", "Unlisted", "Public"])
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output directory")
    return parser.parse_args()


def find_template(start: Path) -> Path | None:
    for base in [start, *start.parents]:
        for name in KNOWN_TUTORIAL_NAMES:
            candidate = base / name / "ModTemplate"
            if (candidate / "ModConfig.json").is_file():
                return candidate
    for candidate in start.rglob("ModTemplate"):
        if (candidate / "ModConfig.json").is_file():
            return candidate
    return None


def main() -> int:
    args = parse_args()
    out_root = Path(args.out).resolve()
    template = Path(args.template).resolve() if args.template else find_template(out_root)
    if template is None:
        raise SystemExit(
            "ModTemplate not found. Run scripts/ensure_tutorial.py --root <workspace-root> "
            "or pass --template <path-to-ModTemplate>."
        )
    target = out_root / args.name

    if not template.is_dir():
        raise SystemExit(f"Template not found: {template}")
    if not (template / "ModConfig.json").is_file():
        raise SystemExit(f"Template missing ModConfig.json: {template}")
    if target.exists():
        if not args.force:
            raise SystemExit(f"Target already exists, pass --force to overwrite: {target}")
        shutil.rmtree(target)

    shutil.copytree(template, target)

    config_path = target / "ModConfig.json"
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    config.update(
        {
            "ModName": args.name,
            "ModVersion": args.version,
            "ModAuthor": args.author,
            "ModDescription": args.description,
            "IconPath": config.get("IconPath") or "Icon.png",
            "Enabled": True,
            "Dependencies": config.get("Dependencies"),
            "WorkshopVisibility": args.visibility,
        }
    )
    config.setdefault("PublishedFileId", "")
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
