#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" / "assets"
MANIFEST = PUBLIC / "manifest.json"
REQUIRED_STATES = ["alive", "warming", "burning", "inferno", "burnt", "recovering"]
REQUIRED_ALIVE_TIMES = ["day", "evening", "night"]
REQUIRED_ALPHA = [
    PUBLIC / "fx" / "smoke" / "smoke_light_01.png",
    PUBLIC / "fx" / "smoke" / "smoke_heavy_01.png",
    PUBLIC / "fx" / "fire" / "fire_small_01.png",
    PUBLIC / "fx" / "fire" / "fire_roof_01.png",
    PUBLIC / "fx" / "fire" / "fire_large_01.png",
    PUBLIC / "fx" / "particles" / "ember_01.png",
    PUBLIC / "fx" / "particles" / "ash_01.png",
    PUBLIC / "fx" / "particles" / "rain_streak_01.png",
    PUBLIC / "fx" / "birds" / "bird_01.png",
]


def assert_image(path: Path) -> Image.Image:
    if not path.exists():
        raise AssertionError(f"Missing asset: {path}")
    return Image.open(path)


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing manifest. Run python scripts/build_manifest.py")
    manifest = json.loads(MANIFEST.read_text())

    for state in REQUIRED_STATES:
        plate = PUBLIC / "worlds" / "global" / "evening" / state / "world_plate.webp"
        with assert_image(plate) as img:
            if img.size != (1536, 864):
                raise AssertionError(f"Unexpected world plate size for {state}: {img.size}")
            if img.mode not in {"RGB", "RGBA"}:
                raise AssertionError(f"Unexpected image mode for {state}: {img.mode}")
            if not manifest["worlds"]["global"]["evening"].get(state, {}).get("plate"):
                raise AssertionError(f"State missing from manifest: {state}")

    for time_of_day in REQUIRED_ALIVE_TIMES:
        plate = PUBLIC / "worlds" / "global" / time_of_day / "alive" / "world_plate.webp"
        with assert_image(plate) as img:
            if img.size != (1536, 864):
                raise AssertionError(f"Unexpected alive {time_of_day} plate size: {img.size}")
            if not manifest["worlds"]["global"].get(time_of_day, {}).get("alive", {}).get("plate"):
                raise AssertionError(f"Alive {time_of_day} missing from manifest.")

    for path in REQUIRED_ALPHA:
        with assert_image(path) as img:
            if img.mode != "RGBA":
                raise AssertionError(f"Sprite lacks alpha channel: {path}")
            alpha = img.getchannel("A")
            if alpha.getextrema()[0] != 0:
                raise AssertionError(f"Sprite has no transparent pixels: {path}")
            if img.width > 256 or img.height > 256:
                raise AssertionError(f"Sprite is too large for v1 DOM FX: {path} {img.size}")

    if not manifest.get("logo", {}).get("earthOrbit64"):
        raise AssertionError("Logo missing from manifest.")

    print("Asset validation passed.")


if __name__ == "__main__":
    main()
