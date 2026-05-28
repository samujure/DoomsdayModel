#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import PUBLIC_ASSETS, RISK_STATES
from asset_pipeline.processing.pixelize import pixelize


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-pixelize exported state variants consistently.")
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    args = parser.parse_args()
    for state in RISK_STATES:
        path = PUBLIC_ASSETS / "worlds" / args.region / args.time / state / "world_plate.webp"
        if not path.exists():
            continue
        with Image.open(path) as img:
            _, preview = pixelize(img)
        preview.save(path, "WEBP", quality=92, method=6)
        print(f"Re-pixelized {path}")


if __name__ == "__main__":
    main()

