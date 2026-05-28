#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy a selected world plate into public/assets.")
    parser.add_argument("--select", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    args = parser.parse_args()

    source = Path(args.select)
    if not source.is_absolute():
        source = ROOT / source
    if not source.exists():
        raise SystemExit(f"Selected asset not found: {source}")

    output = ROOT / "public" / "assets" / "worlds" / args.region / args.time / args.state / "world_plate.webp"
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)
    print(f"Exported {output}")


if __name__ == "__main__":
    main()

