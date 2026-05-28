#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import PUBLIC_ASSETS
from asset_pipeline.providers.mock_provider import MockProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate mock transparent FX sprites.")
    parser.add_argument("--mock", action="store_true", default=True)
    args = parser.parse_args()
    if not args.mock:
        raise SystemExit("Real FX generation is deferred. Use --mock.")

    generated = MockProvider().generate_fx(PUBLIC_ASSETS / "fx")
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()

