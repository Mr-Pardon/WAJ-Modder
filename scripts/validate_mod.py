#!/usr/bin/env python3
"""Static checks for a Witch's Apocalyptic Journey Lua mod draft."""

from __future__ import annotations

import csv
import json
import re
import struct
import sys
from pathlib import Path


REQUIRED_CONFIG = ["ModName", "ModVersion", "ModAuthor", "ModDescription", "IconPath", "Enabled"]
IMAGE_EXTS = ["", ".png", ".jpg", ".jpeg"]
PLACEHOLDER_RE = re.compile(r"\{(\d+)\}")
BRACE_TOKEN_RE = re.compile(r"\{([^{}]+)\}")


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def row_id(row: list[str]) -> str:
    return row[0].strip() if row else ""


def data_rows(path: Path) -> list[list[str]]:
    rows = read_csv(path)
    return rows[2:] if len(rows) >= 2 else []


def cell(row: list[str], header: list[str], name: str) -> str:
    if name not in header:
        return ""
    index = header.index(name)
    return row[index].strip() if index < len(row) else ""


def runtime_id(mod_name: str, csv_path: Path, raw_id: str) -> str:
    return f"{mod_name}_{csv_path.stem}_{raw_id.lstrip('*')}"


def collect_ids(root: Path, relative: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    base = root / relative
    if not base.is_dir():
        return result
    for path in base.glob("*.csv"):
        for row in data_rows(path):
            rid = row_id(row)
            if rid:
                result[rid.lstrip("*")] = path
    return result


def check_config(root: Path, issues: list[str], warnings: list[str]) -> dict:
    config_path = root / "ModConfig.json"
    if not config_path.is_file():
        issues.append("Missing ModConfig.json")
        return {}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        issues.append(f"Invalid ModConfig.json: {exc}")
        return {}
    for key in REQUIRED_CONFIG:
        if key not in config or config[key] in ("", None):
            issues.append(f"ModConfig missing required field: {key}")
    if config.get("ModName") and root.name != config.get("ModName"):
        warnings.append(f"Folder name '{root.name}' differs from ModName '{config.get('ModName')}'")
    icon = config.get("IconPath")
    if icon and not (root / icon).is_file():
        warnings.append(f"IconPath does not exist: {icon}")
    return config


def check_csvs(root: Path, issues: list[str], warnings: list[str]) -> None:
    for path in list((root / "Data").rglob("*.csv")) + list((root / "Text").rglob("*.csv")):
        try:
            rows = read_csv(path)
        except Exception as exc:  # noqa: BLE001
            issues.append(f"Cannot read CSV {path.relative_to(root)}: {exc}")
            continue
        if not rows or not rows[0] or rows[0][0] != "Id":
            issues.append(f"CSV missing Id header: {path.relative_to(root)}")
        if len(rows) < 2:
            warnings.append(f"CSV has no comment row: {path.relative_to(root)}")
            continue
        width = len(rows[0])
        seen: set[str] = set()
        for row_number, row in enumerate(rows[2:], start=3):
            rid = row_id(row)
            if len(row) < width:
                warnings.append(
                    f"CSV row {row_number} width {len(row)} is shorter than header width {width}: {path.relative_to(root)}"
                )
            if rid:
                normalized = rid.lstrip("*")
                if normalized in seen:
                    issues.append(f"Duplicate Id '{rid}' in {path.relative_to(root)}")
                seen.add(normalized)
            script = ",".join(row)
            if "(() =>" in script or "=> {" in script:
                issues.append(f"C# lambda syntax found in CSV script row {row_number}: {path.relative_to(root)}")


def check_cards(root: Path, issues: list[str], warnings: list[str]) -> None:
    text_placeholders = collect_card_text_placeholders(root)
    for path in (root / "Data" / "Card").glob("*.csv") if (root / "Data" / "Card").is_dir() else []:
        rows = read_csv(path)
        header = rows[0] if rows else []
        if "InitScript" not in header:
            issues.append(f"Card CSV missing InitScript: {path.relative_to(root)}")
            continue
        init_index = header.index("InitScript")
        for row in rows[2:]:
            rid = row_id(row)
            if not rid:
                continue
            init = row[init_index] if init_index < len(row) else ""
            if "BaseScript" not in init:
                warnings.append(f"Card '{rid}' missing BaseScript in {path.relative_to(root)}")
            has_descriptions = "AddDescription" in init
            placeholders = text_placeholders.get(rid.lstrip("*"), set())
            if placeholders and not has_descriptions:
                warnings.append(
                    f"Card '{rid}' Text/Card uses dynamic placeholders {format_placeholders(placeholders)} "
                    f"but InitScript has no AddDescription"
                )
            if has_descriptions and not placeholders:
                warnings.append(
                    f"Card '{rid}' InitScript registers AddDescription values but matching Text/Card row "
                    "does not use {0}/{1} placeholders"
                )


def collect_card_text_placeholders(root: Path) -> dict[str, set[int]]:
    result: dict[str, set[int]] = {}
    base = root / "Text" / "Card"
    if not base.is_dir():
        return result
    for path in base.glob("*.csv"):
        rows = read_csv(path)
        header = rows[0] if rows else []
        description_indexes = [
            index
            for index, name in enumerate(header)
            if name == "Description" or name.startswith("Description_")
        ]
        for row in rows[2:]:
            rid = row_id(row).lstrip("*")
            if not rid:
                continue
            placeholders: set[int] = set()
            for index in description_indexes:
                if index < len(row):
                    placeholders.update(int(match) for match in PLACEHOLDER_RE.findall(row[index]))
            if placeholders:
                result.setdefault(rid, set()).update(placeholders)
    return result


def format_placeholders(values: set[int]) -> str:
    return ", ".join(f"{{{value}}}" for value in sorted(values))


def collect_local_runtime_refs(root: Path, mod_name: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for base_name in ["Data", "Text"]:
        base = root / base_name
        if not base.is_dir():
            continue
        for path in base.rglob("*.csv"):
            for row in data_rows(path):
                rid = row_id(row).lstrip("*")
                if not rid:
                    continue
                result.setdefault(rid, []).append(runtime_id(mod_name, path, rid))
    return result


def check_text_runtime_refs(root: Path, mod_name: str, warnings: list[str]) -> None:
    local_refs = collect_local_runtime_refs(root, mod_name)
    if not (root / "Text").is_dir():
        return
    for path in (root / "Text").rglob("*.csv"):
        rows = read_csv(path)
        header = rows[0] if rows else []
        description_indexes = [
            index
            for index, name in enumerate(header)
            if name in {"Description", "Note"} or name.startswith("Description_")
        ]
        for row_number, row in enumerate(rows[2:], start=3):
            rid = row_id(row)
            for index in description_indexes:
                if index >= len(row):
                    continue
                for token in BRACE_TOKEN_RE.findall(row[index]):
                    token = token.strip()
                    if not token or token.isdigit():
                        continue
                    if "_" not in token:
                        candidates = local_refs.get(token.lstrip("*"), [])
                        hint = f"; local candidate(s): {', '.join(candidates[:3])}" if candidates else ""
                        warnings.append(
                            f"Text rich reference '{{{token}}}' in {path.relative_to(root)} row {row_number} "
                            f"looks like a bare id; use <CsvFileName>_<RawId> for original content or "
                            f"{mod_name}_<CsvFileName>_<RawId> for mod content{hint}"
                        )


def resolve_mod_image_path(root: Path, mod_name: str, value: str) -> Path | None:
    if not value:
        return None
    normalized = value.replace("\\", "/")
    if normalized.startswith("Mods/"):
        parts = normalized.split("/")
        if len(parts) >= 3 and parts[1] == mod_name:
            rel = "/".join(parts[2:])
            base = root / rel
        else:
            return None
    elif normalized.startswith("ModResource/"):
        base = root / normalized
    else:
        return None
    for ext in IMAGE_EXTS:
        candidate = Path(str(base) + ext) if ext and base.suffix.lower() not in [".png", ".jpg", ".jpeg"] else base
        if candidate.is_file():
            return candidate
    return base


def resolve_image(root: Path, mod_name: str, value: str) -> bool:
    resolved = resolve_mod_image_path(root, mod_name, value)
    return resolved is None or resolved.is_file()


def image_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data.startswith(b"\xff\xd8"):
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            i += 2
            if marker in {0xD8, 0xD9}:
                continue
            if i + 2 > len(data):
                break
            length = struct.unpack(">H", data[i : i + 2])[0]
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                if i + 7 <= len(data):
                    height = struct.unpack(">H", data[i + 3 : i + 5])[0]
                    width = struct.unpack(">H", data[i + 5 : i + 7])[0]
                    return width, height
            i += length
    return None


def check_images(root: Path, mod_name: str, warnings: list[str]) -> None:
    image_fields = {"Icon", "BackIcon", "Image", "Avatar", "Character", "CareerImage", "ActionImage1", "ActionImage2"}
    for path in list((root / "Data").rglob("*.csv")) + list((root / "Text").rglob("*.csv")):
        rows = read_csv(path)
        header = rows[0] if rows else []
        fields = [name for name in image_fields if name in header]
        if not fields:
            continue
        for row in rows[2:]:
            rid = row_id(row)
            for name in fields:
                value = cell(row, header, name)
                if value and not resolve_image(root, mod_name, value):
                    warnings.append(f"Image path for {path.relative_to(root)} row '{rid}' field '{name}' not found: {value}")


def check_card_pack_covers(root: Path, mod_name: str, warnings: list[str]) -> None:
    for base in [root / "Data" / "CardPack", root / "Text" / "CardPack"]:
        if not base.is_dir():
            continue
        for path in base.glob("*.csv"):
            rows = read_csv(path)
            header = rows[0] if rows else []
            if "Icon" not in header:
                continue
            for row in rows[2:]:
                rid = row_id(row)
                value = cell(row, header, "Icon")
                resolved = resolve_mod_image_path(root, mod_name, value)
                if resolved is None or not resolved.is_file():
                    continue
                size = image_size(resolved)
                if size is None:
                    continue
                width, height = size
                ratio = width / height if height else 0
                if height <= width:
                    warnings.append(
                        f"CardPack '{rid}' Icon should be portrait cover art, not square/landscape: "
                        f"{value} is {width}x{height}"
                    )
                elif not 0.60 <= ratio <= 0.72:
                    warnings.append(
                        f"CardPack '{rid}' Icon aspect ratio looks unusual for a cover: "
                        f"{value} is {width}x{height}"
                    )


def check_buff_icons(root: Path, mod_name: str, warnings: list[str]) -> None:
    base = root / "Data" / "Buff"
    if not base.is_dir():
        return
    for path in base.glob("*.csv"):
        rows = read_csv(path)
        header = rows[0] if rows else []
        if "Icon" not in header:
            continue
        for row in rows[2:]:
            rid = row_id(row)
            value = cell(row, header, "Icon")
            resolved = resolve_mod_image_path(root, mod_name, value)
            if resolved is None or not resolved.is_file():
                continue
            size = image_size(resolved)
            if size is None:
                continue
            width, height = size
            if (width, height) != (31, 31):
                warnings.append(
                    f"Buff '{rid}' Icon should be a 31x31 final PNG, not raw generated art: "
                    f"{value} is {width}x{height}"
                )


def check_relic_icons(root: Path, mod_name: str, warnings: list[str]) -> None:
    base = root / "Data" / "Relic"
    if not base.is_dir():
        return
    for path in base.glob("*.csv"):
        rows = read_csv(path)
        header = rows[0] if rows else []
        if "Icon" not in header:
            continue
        for row in rows[2:]:
            rid = row_id(row)
            value = cell(row, header, "Icon")
            resolved = resolve_mod_image_path(root, mod_name, value)
            if resolved is None or not resolved.is_file():
                continue
            size = image_size(resolved)
            if size is None:
                continue
            width, height = size
            if (width, height) != (128, 128):
                warnings.append(
                    f"Relic '{rid}' Icon should be a 128x128 final PNG, not raw generated art: "
                    f"{value} is {width}x{height}"
                )


def check_data_text_pairs(root: Path, warnings: list[str]) -> None:
    for name in ["Card", "Buff", "Relic", "Blessing", "Item", "EnemyCard", "Enemy"]:
        data_ids = collect_ids(root, f"Data/{name}")
        text_ids = collect_ids(root, f"Text/{name}")
        for rid in sorted(data_ids.keys() - text_ids.keys()):
            warnings.append(f"Data/{name} id has no matching Text row: {rid}")
        for rid in sorted(text_ids.keys() - data_ids.keys()):
            warnings.append(f"Text/{name} id has no matching Data row: {rid}")


def check_pack_belong(root: Path, mod_name: str, warnings: list[str]) -> None:
    pack_ids: set[str] = set()
    pack_dir = root / "Data" / "CardPack"
    if pack_dir.is_dir():
        for path in pack_dir.glob("*.csv"):
            for row in data_rows(path):
                rid = row_id(row)
                if rid:
                    pack_ids.add(runtime_id(mod_name, path, rid))
    if not pack_ids:
        return

    for folder in ["Card", "Relic"]:
        base = root / "Data" / folder
        if not base.is_dir():
            continue
        for path in base.glob("*.csv"):
            rows = read_csv(path)
            header = rows[0] if rows else []
            if "PackBelong" not in header:
                warnings.append(f"Data/{folder} has no PackBelong column for card-pack mod: {path.relative_to(root)}")
                continue
            for row in rows[2:]:
                rid = row_id(row)
                if not rid:
                    continue
                pack = cell(row, header, "PackBelong")
                if not pack and folder == "Relic":
                    warnings.append(f"Relic '{rid}' has empty PackBelong and may appear in an official/basic pack")
                elif pack and pack not in pack_ids:
                    warnings.append(f"{folder} '{rid}' PackBelong does not match a local runtime card pack id: {pack}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_mod.py <mod-dir>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    issues: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    config = check_config(root, issues, warnings)
    check_csvs(root, issues, warnings)
    check_cards(root, issues, warnings)
    check_data_text_pairs(root, warnings)
    mod_name = str(config.get("ModName") or root.name)
    check_text_runtime_refs(root, mod_name, warnings)
    check_pack_belong(root, mod_name, warnings)
    check_images(root, mod_name, warnings)
    check_card_pack_covers(root, mod_name, warnings)
    check_buff_icons(root, mod_name, warnings)
    check_relic_icons(root, mod_name, warnings)
    for issue in issues:
        print(f"ERROR: {issue}")
    for warning in warnings:
        print(f"WARN: {warning}")
    if not issues and not warnings:
        print("OK")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
