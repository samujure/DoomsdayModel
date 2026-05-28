#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.sprites.packer import pack_horizontal


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack PNG frames into a horizontal spritesheet.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    frames = sorted(Path(args.input_dir).glob("*.png"))
    if not frames:
        raise SystemExit("No PNG frames found.")
    print(pack_horizontal(frames, Path(args.output)))


if __name__ == "__main__":
    main()

