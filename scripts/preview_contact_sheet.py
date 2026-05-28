#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" / "assets"
OUT = ROOT / "assets_source" / "contact_sheet.png"


def main() -> None:
    paths = sorted((PUBLIC / "worlds" / "global" / "evening").glob("*/world_plate.webp"))
    thumbs = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        img.thumbnail((256, 144), Image.Resampling.NEAREST)
        thumbs.append((path.parent.name, img.copy()))
    if not thumbs:
        raise SystemExit("No world plates found.")
    sheet = Image.new("RGB", (256 * len(thumbs), 174), (8, 10, 24))
    draw = ImageDraw.Draw(sheet)
    for idx, (label, img) in enumerate(thumbs):
        x = idx * 256
        sheet.paste(img, (x, 0))
        draw.text((x + 8, 150), label, fill=(240, 220, 190))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

