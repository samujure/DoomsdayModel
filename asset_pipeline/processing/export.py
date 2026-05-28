from __future__ import annotations

from pathlib import Path

from PIL import Image


def export_webp(image: Image.Image, path: Path, *, quality: int = 92) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", quality=quality, method=6)
    return path


def export_png(image: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG")
    return path

