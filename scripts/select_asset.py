#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a candidate asset by copying it to assets_source/selected.")
    parser.add_argument("candidate")
    parser.add_argument("--name")
    args = parser.parse_args()
    source = Path(args.candidate)
    if not source.is_absolute():
        source = ROOT / source
    if not source.exists():
        raise SystemExit(f"Candidate not found: {source}")
    output = ROOT / "assets_source" / "selected" / (args.name or source.name)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, output)
    print(f"Selected {output}")


if __name__ == "__main__":
    main()

