#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import PUBLIC_ASSETS, RISK_STATES, TIMES_OF_DAY, WORLD_EXPORT_SIZE
from asset_pipeline.providers.mock_provider import MockProvider


ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate mock assets for the website shell.")
    parser.add_argument("--mock", action="store_true", help="Generate deterministic mock assets.")
    parser.add_argument("--target", choices=["all", "logo", "worlds", "fx"], default="all")
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--width", type=int, default=WORLD_EXPORT_SIZE[0])
    parser.add_argument("--height", type=int, default=WORLD_EXPORT_SIZE[1])
    args = parser.parse_args()

    if not args.mock:
        raise SystemExit("This milestone is mock-first. Re-run with --mock.")

    provider = MockProvider()

    if args.target in {"all", "logo"}:
        for path in provider.generate_logo(PUBLIC_ASSETS / "logo"):
            print(f"Generated logo: {path}")

    if args.target in {"all", "worlds"}:
        alive_times = TIMES_OF_DAY if args.target == "all" and args.time == "evening" else [args.time]
        for offset, time_of_day in enumerate(alive_times):
            run(
                "generate_master_alive.py",
                "--region",
                args.region,
                "--time",
                time_of_day,
                "--seed",
                str(args.seed + offset * 10),
                "--width",
                str(args.width),
                "--height",
                str(args.height),
                "--mock",
                "true",
            )
        for idx, state in enumerate([s for s in RISK_STATES if s != "alive"], start=1):
            run(
                "derive_state_variant.py",
                "--region",
                args.region,
                "--time",
                args.time,
                "--state",
                state,
                "--seed",
                str(args.seed + idx),
                "--mock",
                "true",
            )

    if args.target in {"all", "fx"}:
        for path in provider.generate_fx(PUBLIC_ASSETS / "fx"):
            print(f"Generated fx: {path}")

    run("build_manifest.py")
    print("Mock asset pipeline complete.")


if __name__ == "__main__":
    main()
