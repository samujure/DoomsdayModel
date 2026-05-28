#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import ASSETS_SOURCE, PUBLIC_ASSETS, RISK_STATES, WORLD_EXPORT_SIZE
from asset_pipeline.providers.mock_provider import MockProvider


def parse_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive a state variant from the master alive composition.")
    parser.add_argument("--input", default=str(ASSETS_SOURCE / "selected" / "master_alive.png"))
    parser.add_argument("--state", required=True, choices=RISK_STATES)
    parser.add_argument("--region", default="global")
    parser.add_argument("--time", default="evening")
    parser.add_argument("--strength", type=float, default=0.35)
    parser.add_argument("--seed", type=int, default=201)
    parser.add_argument("--mock", type=parse_bool, default=True)
    args = parser.parse_args()

    if not args.mock:
        raise SystemExit("SDXL img2img is deferred for GPU handoff. Run with --mock true on this machine.")

    provider = MockProvider()
    input_path = Path(args.input)
    raw = ASSETS_SOURCE / "generated_raw" / f"world_{args.region}_{args.time}_{args.state}_seed{args.seed}.png"
    public = PUBLIC_ASSETS / "worlds" / args.region / args.time / args.state / "world_plate.webp"
    provider.derive_state_variant(input_path, raw, state=args.state, seed=args.seed, strength=args.strength, time_of_day=args.time)
    provider.derive_state_variant(input_path, public, state=args.state, seed=args.seed, strength=args.strength, time_of_day=args.time)
    print(f"Generated mock state variant: {public}")


if __name__ == "__main__":
    main()
