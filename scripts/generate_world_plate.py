#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import RISK_STATES, WORLD_EXPORT_SIZE


ROOT = Path(__file__).resolve().parents[1]


def parse_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compatibility wrapper for generating a v1 world plate.")
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    parser.add_argument("--state", default="alive", choices=RISK_STATES)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--width", type=int, default=WORLD_EXPORT_SIZE[0])
    parser.add_argument("--height", type=int, default=WORLD_EXPORT_SIZE[1])
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--mock", type=parse_bool, default=True)
    args = parser.parse_args()

    if args.state == "alive":
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "generate_master_alive.py"),
                "--region",
                args.region,
                "--time",
                args.time,
                "--seed",
                str(args.seed),
                "--width",
                str(args.width),
                "--height",
                str(args.height),
                "--steps",
                str(args.steps),
                "--mock",
                str(args.mock).lower(),
            ],
            check=True,
        )
        return

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "derive_state_variant.py"),
            "--region",
            args.region,
            "--time",
            args.time,
            "--state",
            args.state,
            "--seed",
            str(args.seed),
            "--mock",
            str(args.mock).lower(),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()

