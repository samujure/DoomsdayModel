from __future__ import annotations

from PIL import Image


BAYER_4 = (
    (0, 8, 2, 10),
    (12, 4, 14, 6),
    (3, 11, 1, 9),
    (15, 7, 13, 5),
)


def ordered_bayer_4x4(image: Image.Image, strength: int = 10) -> Image.Image:
    img = image.convert("RGB").copy()
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            threshold = (BAYER_4[y % 4][x % 4] - 7.5) * strength
            r, g, b = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, int(r + threshold))),
                max(0, min(255, int(g + threshold))),
                max(0, min(255, int(b + threshold))),
            )
    return img

