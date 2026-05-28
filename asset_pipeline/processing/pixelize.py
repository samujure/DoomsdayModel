from __future__ import annotations

from PIL import Image


def pixelize(
    image: Image.Image,
    *,
    pixel_width: int = 512,
    pixel_height: int = 288,
    export_scale: int = 3,
    resample_down: str = "bicubic",
) -> tuple[Image.Image, Image.Image]:
    down_filter = Image.Resampling.BICUBIC if resample_down == "bicubic" else Image.Resampling.BILINEAR
    small = image.resize((pixel_width, pixel_height), down_filter)
    preview = small.resize((pixel_width * export_scale, pixel_height * export_scale), Image.Resampling.NEAREST)
    return small, preview

