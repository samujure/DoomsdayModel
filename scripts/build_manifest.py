#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asset_pipeline.config import PUBLIC_ASSETS, RISK_STATES, TIMES_OF_DAY


def asset_url(path: Path) -> str:
    return "/" + path.relative_to(PUBLIC_ASSETS.parent).as_posix()


def image_ok(path: Path) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def main() -> None:
    worlds: dict[str, dict] = {"global": {}}
    for time_of_day in TIMES_OF_DAY:
        worlds["global"][time_of_day] = {}
        for state in RISK_STATES:
            plate = PUBLIC_ASSETS / "worlds" / "global" / time_of_day / state / "world_plate.webp"
            if plate.exists() and image_ok(plate):
                worlds["global"][time_of_day][state] = {"plate": asset_url(plate)}

    logo = {}
    for size in [32, 64, 128, 256]:
        path = PUBLIC_ASSETS / "logo" / f"earth_orbit_{size}.png"
        if path.exists() and image_ok(path):
            logo[f"earthOrbit{size}"] = asset_url(path)

    def list_pngs(folder: str) -> list[str]:
        root = PUBLIC_ASSETS / "fx" / folder
        if not root.exists():
            return []
        return [asset_url(path) for path in sorted(root.glob("*.png")) if image_ok(path)]

    particles = {}
    for key, filename in {
        "ember": "ember_01.png",
        "ash": "ash_01.png",
        "rain": "rain_streak_01.png",
    }.items():
        path = PUBLIC_ASSETS / "fx" / "particles" / filename
        if path.exists() and image_ok(path):
            particles[key] = asset_url(path)

    manifest = {
        "logo": logo,
        "worlds": worlds,
        "fx": {
            "clouds": list_pngs("clouds"),
            "smoke": list_pngs("smoke"),
            "fire": list_pngs("fire"),
            "particles": particles,
            "birds": list_pngs("birds"),
        },
    }

    output = PUBLIC_ASSETS / "manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
