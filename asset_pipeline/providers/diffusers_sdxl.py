from __future__ import annotations


class DeferredSDXLProvider:
    """Dormant SDXL boundary for the RTX 4070 handoff.

    This provider intentionally does not import torch or diffusers during the
    mock-first milestone. It exists so scripts have a stable provider seam when
    SDXL generation is enabled later on the GPU machine.
    """

    def __init__(self, *_, **__):
        raise RuntimeError(
            "SDXL generation is deferred until the GPU handoff. "
            "Run scripts with --mock on this machine."
        )

