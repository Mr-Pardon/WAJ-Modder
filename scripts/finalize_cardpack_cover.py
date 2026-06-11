#!/usr/bin/env python3
"""Finalize a Witch's Apocalyptic Journey card-pack cover.

The script converts a generated portrait image into the expected 300x440 PNG,
applies the skill's silhouette alpha mask, clears transparent RGB data, and
removes common green/chroma-key edge remnants. It does not overlay the outer
frame unless --overlay-frame is passed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


SIZE = (300, 440)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def cover_resize(image: Image.Image, mode: str) -> Image.Image:
    image = image.convert("RGBA")
    if mode == "stretch":
        return image.resize(SIZE, Image.Resampling.LANCZOS)

    source_ratio = image.width / image.height
    target_ratio = SIZE[0] / SIZE[1]
    if mode == "crop":
        if source_ratio > target_ratio:
            new_width = int(image.height * target_ratio)
            left = (image.width - new_width) // 2
            image = image.crop((left, 0, left + new_width, image.height))
        elif source_ratio < target_ratio:
            new_height = int(image.width / target_ratio)
            top = (image.height - new_height) // 2
            image = image.crop((0, top, image.width, top + new_height))
        return image.resize(SIZE, Image.Resampling.LANCZOS)

    if mode == "contain":
        scale = min(SIZE[0] / image.width, SIZE[1] / image.height)
        resized = image.resize((max(1, int(image.width * scale)), max(1, int(image.height * scale))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        canvas.alpha_composite(resized, ((SIZE[0] - resized.width) // 2, (SIZE[1] - resized.height) // 2))
        return canvas

    raise ValueError(f"Unknown resize mode: {mode}")


def strip_green_edges(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                pixels[x, y] = (0, 0, 0, 0)
                continue
            is_green_fringe = g > 90 and g > r * 1.35 and g > b * 1.25
            if a < 220 and is_green_fringe:
                pixels[x, y] = (r, g, b, 0)
    return image


def alpha_composite_frame(image: Image.Image, frame_path: Path) -> Image.Image:
    frame = Image.open(frame_path).convert("RGBA").resize(SIZE, Image.Resampling.LANCZOS)
    return Image.alpha_composite(image, frame)


def finalize(input_path: Path, output_path: Path, overlay_frame: bool, resize_mode: str) -> None:
    assets = skill_root() / "assets"
    mask = Image.open(assets / "cardpack-cover-silhouette-300x440.png").convert("RGBA").resize(
        SIZE, Image.Resampling.LANCZOS
    )
    image = cover_resize(Image.open(input_path), resize_mode)
    image.putalpha(mask.getchannel("A"))
    image = strip_green_edges(image)
    if overlay_frame:
        image = alpha_composite_frame(image, assets / "cardpack-cover-frame-300x440.png")
        image = strip_green_edges(image)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize a 300x440 card-pack cover PNG.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--overlay-frame",
        action="store_true",
        help="Overlay the clean outer frame. Off by default to avoid unwanted extra borders.",
    )
    parser.add_argument(
        "--resize-mode",
        choices=["stretch", "crop", "contain"],
        default="stretch",
        help="How to fit generated full-cover art into 300x440. Default stretch preserves all titles and composition.",
    )
    args = parser.parse_args()
    finalize(args.input, args.output, args.overlay_frame, args.resize_mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
