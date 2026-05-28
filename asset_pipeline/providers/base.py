from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ImageProvider(Protocol):
    def generate_master_alive(self, output: Path, *, seed: int, width: int, height: int, time_of_day: str = "evening") -> Path:
        ...

    def derive_state_variant(self, input_path: Path, output: Path, *, state: str, seed: int, strength: float, time_of_day: str = "evening") -> Path:
        ...
