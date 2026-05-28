#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Reject a candidate asset by moving it to assets_source/rejected.")
    parser.add_argument("candidate")
    args = parser.parse_args()
    source = Path(args.candidate)
    if not source.is_absolute():
        source = ROOT / source
    if not source.exists():
        raise SystemExit(f"Candidate not found: {source}")
    output = ROOT / "assets_source" / "rejected" / source.name
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), output)
    print(f"Rejected {output}")


if __name__ == "__main__":
    main()

