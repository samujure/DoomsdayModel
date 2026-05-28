#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.processing.pixelize import pixelize


def main() -> None:
    parser = argparse.ArgumentParser(description="Pixelize an existing image.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pixel-width", type=int, default=512)
    parser.add_argument("--pixel-height", type=int, default=288)
    parser.add_argument("--export-scale", type=int, default=3)
    args = parser.parse_args()

    with Image.open(args.input) as img:
        _, preview = pixelize(
            img,
            pixel_width=args.pixel_width,
            pixel_height=args.pixel_height,
            export_scale=args.export_scale,
        )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(output)
    print(f"Pixelized {output}")


if __name__ == "__main__":
    main()

