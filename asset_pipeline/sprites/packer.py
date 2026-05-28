from __future__ import annotations

from pathlib import Path

from PIL import Image


def pack_horizontal(paths: list[Path], output: Path) -> Path:
    frames = [Image.open(path).convert("RGBA") for path in paths]
    width = sum(frame.width for frame in frames)
    height = max(frame.height for frame in frames)
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 0
    for frame in frames:
        sheet.alpha_composite(frame, (x, 0))
        x += frame.width
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return output

