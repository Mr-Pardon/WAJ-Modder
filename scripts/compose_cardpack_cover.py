#!/usr/bin/env python3
"""Fallback composer for a WAJ card-pack cover from generated center art.

Prefer template-guided full-cover image generation plus finalize_cardpack_cover.py.
Use this script only when a deterministic template/text composition fallback is
needed. The image model should provide text-free center art.
"""

from __future__ import annotations

import argparse
import colorsys
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


SIZE = (300, 440)
CENTER_BOX = (34, 82, 266, 332)
TEMPLATE_CLEAR_BOX = (34, 82, 266, 332)
TEXT_LIGHT = (248, 250, 255, 255)
TEXT_SHADOW = (30, 32, 86, 255)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_color(value: str) -> tuple[int, int, int]:
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid color '{value}'. Use a CSS color or #RRGGBB.") from exc
    return rgb[:3]


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(int(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def default_template_path() -> Path:
    return skill_root() / "assets" / "cardpack-cover-base-300x440.png"


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGBA")
    source_ratio = image.width / image.height
    target_ratio = size[0] / size[1]
    if source_ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        image = image.crop((left, 0, left + new_width, image.height))
    elif source_ratio < target_ratio:
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        image = image.crop((0, top, image.width, top + new_height))
    return image.resize(size, Image.Resampling.LANCZOS)


def find_font(preferred: Path | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: list[Path] = []
    if preferred is not None:
        candidates.append(preferred)
    candidates.extend(
        [
            Path("C:/Windows/Fonts/msyh.ttc"),
            Path("C:/Windows/Fonts/msyhbd.ttc"),
            Path("C:/Windows/Fonts/simhei.ttf"),
            Path("C:/Windows/Fonts/simsun.ttc"),
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/arial.ttf"),
        ]
    )
    for path in candidates:
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_font(text: str, font_path: Path | None, max_width: int, start_size: int, min_size: int) -> ImageFont.ImageFont:
    for size in range(start_size, min_size - 1, -1):
        font = find_font(font_path, size)
        box = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=font, stroke_width=2)
        if box[2] - box[0] <= max_width:
            return font
    return find_font(font_path, min_size)


def wrap_cjk(text: str, max_chars: int) -> list[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


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


def recolor_template(image: Image.Image, theme: tuple[int, int, int], strength: float) -> Image.Image:
    strength = max(0.0, min(1.0, strength))
    if strength == 0:
        return image.convert("RGBA")

    result = image.convert("RGBA")
    pixels = result.load()
    theme_h, _theme_l, theme_s = colorsys.rgb_to_hls(*(channel / 255 for channel in theme))
    for y in range(result.height):
        for x in range(result.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            high = max(r, g, b)
            low = min(r, g, b)
            if high < 44 or high - low < 18:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if s < 0.16:
                continue
            target_s = max(s * 0.75, theme_s * 0.65)
            nr, ng, nb = colorsys.hls_to_rgb(theme_h, l, min(1.0, target_s))
            recolored = (int(nr * 255), int(ng * 255), int(nb * 255))
            pixels[x, y] = (*mix((r, g, b), recolored, strength), a)
    return result


def template_overlay(template: Image.Image) -> Image.Image:
    overlay = template.copy().convert("RGBA")
    pixels = overlay.load()
    x0, y0, x1, y1 = TEMPLATE_CLEAR_BOX
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, _a = pixels[x, y]
            pixels[x, y] = (r, g, b, 0)
    return overlay


def draw_titles(
    image: Image.Image,
    title_zh: str,
    title_en: str,
    font_path: Path | None,
    theme: tuple[int, int, int],
) -> None:
    draw = ImageDraw.Draw(image)
    title_bg = (*mix(theme, (16, 18, 78), 0.82), 235)
    if title_en:
        font_en = fit_font(title_en, font_path, 148, 20, 11)
        box = draw.textbbox((0, 0), title_en, font=font_en, stroke_width=2)
        width = box[2] - box[0]
        x = max(120, 268 - width)
        y = 58
        draw.rounded_rectangle((x - 8, y - 4, min(286, x + width + 10), y + 25), radius=3, fill=title_bg)
        draw.text((x, y), title_en, font=font_en, fill=TEXT_LIGHT, stroke_width=2, stroke_fill=TEXT_SHADOW)

    if title_zh:
        lines = wrap_cjk(title_zh, 5)
        font_zh = fit_font(max(lines, key=len), font_path, 164, 31, 20)
        line_height = max(27, font_zh.size if hasattr(font_zh, "size") else 27)
        x = 48
        y = 333
        boxes = [draw.textbbox((0, 0), line, font=font_zh, stroke_width=3) for line in lines]
        for i, (line, box) in enumerate(zip(lines, boxes)):
            draw.text(
                (x - box[0], y + i * line_height),
                line,
                font=font_zh,
                fill=TEXT_LIGHT,
                stroke_width=3,
                stroke_fill=TEXT_SHADOW,
            )


def compose(
    center_path: Path,
    output_path: Path,
    title_zh: str,
    title_en: str,
    theme_color: str,
    font_path: Path | None,
    template_path: Path,
    template_recolor_strength: float,
) -> None:
    theme = parse_color(theme_color)
    template = Image.open(template_path).convert("RGBA").resize(SIZE, Image.Resampling.NEAREST)
    template = recolor_template(template, theme, template_recolor_strength)
    bg = template.copy()

    center = cover_crop(Image.open(center_path), (CENTER_BOX[2] - CENTER_BOX[0], CENTER_BOX[3] - CENTER_BOX[1]))
    bg.alpha_composite(center, (CENTER_BOX[0], CENTER_BOX[1]))
    bg.alpha_composite(template_overlay(template))

    draw_titles(bg, title_zh, title_en, font_path, theme)

    mask = Image.open(skill_root() / "assets" / "cardpack-cover-silhouette-300x440.png").convert("RGBA").resize(
        SIZE, Image.Resampling.LANCZOS
    )
    bg.putalpha(mask.getchannel("A"))
    bg = strip_green_edges(bg)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a 300x440 WAJ card-pack cover from center art.")
    parser.add_argument("center_art", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title-zh", default="", help="Chinese card-pack title.")
    parser.add_argument("--title-en", default="", help="English card-pack title.")
    parser.add_argument("--theme-color", default="#6db6d6", help="Theme color, for example #6db6d6.")
    parser.add_argument("--font", type=Path, default=None, help="Optional TrueType/OpenType font path.")
    parser.add_argument("--template", type=Path, default=default_template_path(), help="300x440 card-pack base template.")
    parser.add_argument(
        "--template-recolor-strength",
        type=float,
        default=0.72,
        help="0 disables template recoloring; 1 fully shifts saturated template colors toward --theme-color.",
    )
    args = parser.parse_args()
    if not args.center_art.is_file():
        raise SystemExit(f"Center art not found: {args.center_art}")
    if args.font is not None and not args.font.is_file():
        raise SystemExit(f"Font not found: {args.font}")
    if not args.template.is_file():
        raise SystemExit(f"Template not found: {args.template}")
    compose(
        args.center_art,
        args.output,
        args.title_zh,
        args.title_en,
        args.theme_color,
        args.font,
        args.template,
        args.template_recolor_strength,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
