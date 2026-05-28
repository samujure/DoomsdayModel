#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import ASSETS_SOURCE, PUBLIC_ASSETS, WORLD_EXPORT_SIZE
from asset_pipeline.providers.mock_provider import MockProvider


def parse_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the master alive composition.")
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--width", type=int, default=WORLD_EXPORT_SIZE[0])
    parser.add_argument("--height", type=int, default=WORLD_EXPORT_SIZE[1])
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--mock", type=parse_bool, default=True)
    args = parser.parse_args()

    if not args.mock:
        raise SystemExit("SDXL generation is deferred for GPU handoff. Run with --mock true on this machine.")

    provider = MockProvider()
    raw = ASSETS_SOURCE / "generated_raw" / f"master_{args.region}_{args.time}_alive_seed{args.seed}.png"
    selected = ASSETS_SOURCE / "selected" / f"master_{args.time}_alive.png"
    public = PUBLIC_ASSETS / "worlds" / args.region / args.time / "alive" / "world_plate.webp"

    provider.generate_master_alive(raw, seed=args.seed, width=args.width, height=args.height, time_of_day=args.time)
    provider.generate_master_alive(selected, seed=args.seed, width=args.width, height=args.height, time_of_day=args.time)
    provider.generate_master_alive(public, seed=args.seed, width=args.width, height=args.height, time_of_day=args.time)
    if args.time == "evening":
        provider.generate_master_alive(
            ASSETS_SOURCE / "selected" / "master_alive.png",
            seed=args.seed,
            width=args.width,
            height=args.height,
            time_of_day=args.time,
        )
    print(f"Generated mock master alive: {public}")


if __name__ == "__main__":
    main()
