from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ASSETS = ROOT / "public" / "assets"
ASSETS_SOURCE = ROOT / "assets_source"

REGIONS = ["global"]
TIMES_OF_DAY = ["day", "evening", "night"]
RISK_STATES = ["alive", "warming", "burning", "inferno", "burnt", "recovering"]

WORLD_LOW_RES = (512, 288)
WORLD_EXPORT_SCALE = 3
WORLD_EXPORT_SIZE = (WORLD_LOW_RES[0] * WORLD_EXPORT_SCALE, WORLD_LOW_RES[1] * WORLD_EXPORT_SCALE)

STATE_PALETTES = {
    "alive": {
        "sky_top": "#090d28",
        "sky_mid": "#532464",
        "sky_low": "#f27a55",
        "sun": "#ffd98a",
        "water": "#182d5a",
        "window": "#ffd36b",
        "accent": "#45d0ff",
        "haze": "#6c4bb6",
    },
    "warming": {
        "sky_top": "#100717",
        "sky_mid": "#4b1830",
        "sky_low": "#b6422c",
        "sun": "#d96936",
        "water": "#21172d",
        "window": "#ff9248",
        "accent": "#c24c35",
        "haze": "#2a151b",
    },
    "burning": {
        "sky_top": "#170713",
        "sky_mid": "#8a203d",
        "sky_low": "#ff4b2f",
        "sun": "#ff8a36",
        "water": "#32152f",
        "window": "#ff5d31",
        "accent": "#ffcd5a",
        "haze": "#b12a2a",
    },
    "inferno": {
        "sky_top": "#07040a",
        "sky_mid": "#5b0c21",
        "sky_low": "#e01f1f",
        "sun": "#ff472f",
        "water": "#1a0b17",
        "window": "#ff2c1e",
        "accent": "#ffd45c",
        "haze": "#2c0b12",
    },
    "burnt": {
        "sky_top": "#080307",
        "sky_mid": "#4f0b19",
        "sky_low": "#e43b21",
        "sun": "#ff6a2c",
        "water": "#16080d",
        "window": "#ff3a20",
        "accent": "#ffce57",
        "haze": "#1f070d",
    },
    "recovering": {
        "sky_top": "#06172b",
        "sky_mid": "#174063",
        "sky_low": "#4b947e",
        "sun": "#c3e8ca",
        "water": "#103451",
        "window": "#9ef0bf",
        "accent": "#59d6ff",
        "haze": "#4e8aa1",
    },
}

FX_MANIFEST = {
    "clouds": ["cloud_01.png", "cloud_02.png", "cloud_03.png"],
    "smoke": ["smoke_light_01.png", "smoke_heavy_01.png"],
    "fire": ["fire_small_01.png", "fire_roof_01.png", "fire_large_01.png"],
    "particles": ["ember_01.png", "ash_01.png", "rain_streak_01.png"],
    "birds": ["bird_01.png"],
}
