from __future__ import annotations

from PIL import Image


def reduce_palette(image: Image.Image, *, colors: int = 48, method: str = "mediancut", dither: bool = False) -> Image.Image:
    if image.mode == "RGBA":
        alpha = image.getchannel("A")
        rgb = image.convert("RGB")
    else:
        alpha = None
        rgb = image.convert("RGB")

    method_map = {
        "mediancut": Image.Quantize.MEDIANCUT,
        "fastoctree": Image.Quantize.FASTOCTREE,
    }
    quantized = rgb.quantize(
        colors=colors,
        method=method_map.get(method, Image.Quantize.MEDIANCUT),
        dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE,
    ).convert("RGB")
    if alpha:
        quantized.putalpha(alpha)
    return quantized

