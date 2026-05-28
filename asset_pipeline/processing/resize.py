from __future__ import annotations

from PIL import Image, ImageOps


def resize_image(image: Image.Image, size: tuple[int, int], mode: str = "contain") -> Image.Image:
    if mode == "stretch":
        return image.resize(size, Image.Resampling.BICUBIC)
    if mode == "fit":
        return ImageOps.fit(image, size, method=Image.Resampling.BICUBIC)
    if mode == "contain":
        return ImageOps.contain(image, size, method=Image.Resampling.BICUBIC)
    raise ValueError(f"Unsupported resize mode: {mode}")

