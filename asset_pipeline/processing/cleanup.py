from __future__ import annotations

from collections import Counter

from PIL import Image, ImageFilter


def cleanup_rare_colors(image: Image.Image, *, min_color_count: int = 12, median_filter: bool = False) -> Image.Image:
    img = image.convert("RGBA")
    pixels = list(img.getdata())
    counts = Counter(pixels)
    common = [color for color, count in counts.items() if count >= min_color_count]
    if not common:
        return img

    def nearest(color: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        if color[3] == 0:
            return color
        return min(common, key=lambda c: sum((color[i] - c[i]) ** 2 for i in range(3)))

    img.putdata([p if counts[p] >= min_color_count else nearest(p) for p in pixels])
    if median_filter:
        img = img.filter(ImageFilter.MedianFilter(size=3))
    return img

