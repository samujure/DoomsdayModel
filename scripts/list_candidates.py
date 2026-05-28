#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for path in sorted((ROOT / "assets_source" / "candidates").glob("**/*")):
    if path.is_file():
        print(path.relative_to(ROOT))

