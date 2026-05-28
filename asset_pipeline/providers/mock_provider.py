from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from asset_pipeline.config import STATE_PALETTES, WORLD_EXPORT_SCALE, WORLD_LOW_RES


class MockProvider:
    """Deterministic mock pixel-art provider.

    The world composition is intentionally shared across all states: mountains,
    bridge, skyline, domes, river, and foreground keep the same positions while
    atmosphere and damage details change.
    """

    def generate_master_alive(self, output: Path, *, seed: int, width: int, height: int, time_of_day: str = "evening") -> Path:
        image = self._draw_world("alive", seed=seed, time_of_day=time_of_day)
        return self._save_world(image, output, width=width, height=height)

    def derive_state_variant(self, input_path: Path, output: Path, *, state: str, seed: int, strength: float, time_of_day: str = "evening") -> Path:
        image = self._draw_world(state, seed=seed, time_of_day=time_of_day)
        width, height = WORLD_LOW_RES[0] * WORLD_EXPORT_SCALE, WORLD_LOW_RES[1] * WORLD_EXPORT_SCALE
        if input_path.exists():
            with Image.open(input_path) as base:
                width, height = base.size
        return self._save_world(image, output, width=width, height=height)

    def generate_logo(self, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        generated = []
        base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(base)

        draw.ellipse((9, 9, 119, 119), fill=(72, 31, 126, 255), outline=(170, 92, 255, 255), width=5)
        draw.ellipse((31, 34, 94, 97), fill=(43, 183, 214, 255), outline=(192, 245, 255, 255), width=3)
        draw.polygon([(45, 41), (58, 36), (70, 45), (66, 55), (50, 55)], fill=(88, 222, 127, 255))
        draw.polygon([(68, 62), (84, 60), (89, 72), (77, 85), (64, 78)], fill=(82, 211, 116, 255))
        draw.polygon([(39, 68), (53, 70), (55, 86), (42, 88), (34, 78)], fill=(65, 191, 104, 255))

        ring = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ring_draw = ImageDraw.Draw(ring)
        ring_draw.ellipse((15, 46, 113, 85), outline=(226, 203, 255, 255), width=4)
        ring = ring.rotate(-18, resample=Image.Resampling.NEAREST)
        base.alpha_composite(ring)
        draw = ImageDraw.Draw(base)
        draw.arc((15, 46, 113, 85), start=198, end=345, fill=(116, 61, 203, 255), width=5)

        for size in [32, 64, 128, 256]:
            img = base.resize((size, size), Image.Resampling.NEAREST)
            path = output_dir / f"earth_orbit_{size}.png"
            img.save(path)
            generated.append(path)

        preview = base.resize((256, 256), Image.Resampling.NEAREST)
        preview.save(output_dir / "logo_preview.png")
        return generated

    def generate_fx(self, fx_dir: Path) -> list[Path]:
        generated: list[Path] = []
        generated.extend(self._clouds(fx_dir / "clouds"))
        generated.extend(self._smoke(fx_dir / "smoke"))
        generated.extend(self._fire(fx_dir / "fire"))
        generated.extend(self._particles(fx_dir / "particles"))
        generated.extend(self._birds(fx_dir / "birds"))
        return generated

    def _draw_world(self, state: str, *, seed: int, time_of_day: str = "evening") -> Image.Image:
        rng = random.Random(seed)
        palette = dict(STATE_PALETTES[state])
        if state == "alive":
            palette.update(self._alive_time_palette(time_of_day))
        width, height = WORLD_LOW_RES
        img = Image.new("RGB", (width, height), palette["sky_top"])
        draw = ImageDraw.Draw(img)

        self._gradient(draw, width, height, palette["sky_top"], palette["sky_mid"], 0, 168)
        self._gradient(draw, width, height, palette["sky_mid"], palette["sky_low"], 108, 212)

        sun_color = self._hex(palette["sun"])
        draw.ellipse((104, 80, 154, 130), fill=sun_color)
        for y in range(95, 127, 8):
            draw.rectangle((102, y, 158, y + 3), fill=self._hex(palette["sky_low"]))

        star_color = (114, 128, 222)
        if state in {"alive", "recovering"} and time_of_day != "day":
            for _ in range(52):
                x = rng.randrange(0, width)
                y = rng.randrange(6, 96)
                draw.rectangle((x, y, x + 1, y + 1), fill=star_color)

        self._cloud_bands(draw, state, palette)
        self._mountains(draw, palette)
        self._river(draw, palette)
        self._bridge(draw, palette)
        self._city(draw, state, palette)
        self._domes(draw, state, palette)
        self._foreground(draw, state, palette)
        self._state_overlays(draw, state, palette)
        self._dither_pixels(draw, state, rng)
        return img

    def _alive_time_palette(self, time_of_day: str) -> dict[str, str]:
        palettes = {
            "day": {
                "sky_top": "#4a86d9",
                "sky_mid": "#6fb6e8",
                "sky_low": "#ffd37a",
                "sun": "#fff1a8",
                "water": "#2e73a8",
                "window": "#f8f1b2",
                "accent": "#48c9ff",
                "haze": "#d8a6cf",
            },
            "night": {
                "sky_top": "#030617",
                "sky_mid": "#0b1232",
                "sky_low": "#22164f",
                "sun": "#d8e8ff",
                "water": "#07152f",
                "window": "#ffd56a",
                "accent": "#5fd7ff",
                "haze": "#36236d",
            },
            "evening": STATE_PALETTES["alive"],
        }
        return palettes.get(time_of_day, palettes["evening"])

    def _save_world(self, image: Image.Image, output: Path, *, width: int, height: int) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        scaled = image.resize((width, height), Image.Resampling.NEAREST)
        if output.suffix.lower() == ".webp":
            scaled.save(output, quality=92, method=6)
        else:
            scaled.save(output)
        return output

    def _gradient(self, draw: ImageDraw.ImageDraw, width: int, _height: int, top: str, bottom: str, y0: int, y1: int) -> None:
        c0 = self._hex(top)
        c1 = self._hex(bottom)
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0 - 1)
            color = tuple(int(c0[i] * (1 - t) + c1[i] * t) for i in range(3))
            draw.line((0, y, width, y), fill=color)

    def _cloud_bands(self, draw: ImageDraw.ImageDraw, state: str, palette: dict[str, str]) -> None:
        cloud = self._hex(palette["haze"])
        alt = self._mix(cloud, self._hex(palette["sky_low"]), 0.35)
        bands = [(8, 44, 96), (305, 46, 88), (30, 92, 60), (365, 91, 72)]
        for x, y, w in bands:
            for i in range(0, w, 10):
                h = 5 + (i % 18)
                draw.rectangle((x + i, y - h // 2, x + i + 14, y + h // 2), fill=cloud if i % 3 else alt)
        if state in {"warming", "burning", "inferno", "burnt"}:
            smoke = (22, 15, 18) if state == "warming" else (26, 10, 15) if state in {"inferno", "burnt"} else (48, 35, 43)
            smoke_bands = [(250, 74, 70), (352, 55, 100), (410, 82, 75)]
            if state == "warming":
                smoke_bands = [(282, 88, 46), (338, 70, 58), (425, 96, 42)]
            if state == "burnt":
                smoke_bands.extend([(170, 92, 92), (294, 44, 132), (36, 116, 115)])
            for x, y, w in smoke_bands:
                for i in range(0, w, 8):
                    draw.rectangle((x + i, y - (i % 21), x + i + 18, y + 6), fill=smoke)

    def _mountains(self, draw: ImageDraw.ImageDraw, palette: dict[str, str]) -> None:
        far = self._mix(self._hex(palette["sky_mid"]), (22, 24, 65), 0.48)
        near = self._mix(self._hex(palette["sky_top"]), (48, 39, 84), 0.54)
        draw.polygon([(0, 150), (60, 104), (117, 152), (178, 105), (250, 150), (315, 98), (405, 151), (512, 93), (512, 184), (0, 184)], fill=far)
        draw.polygon([(0, 170), (72, 125), (128, 174), (200, 119), (276, 172), (338, 127), (420, 176), (512, 118), (512, 195), (0, 195)], fill=near)

    def _river(self, draw: ImageDraw.ImageDraw, palette: dict[str, str]) -> None:
        water = self._hex(palette["water"])
        draw.polygon([(0, 194), (512, 184), (512, 288), (0, 288)], fill=water)
        reflection = self._mix(water, self._hex(palette["sun"]), 0.35)
        for y in range(196, 252, 10):
            draw.rectangle((108 - (y - 196), y, 180 + (y - 196), y + 2), fill=reflection)
        for x in range(0, 512, 22):
            draw.rectangle((x, 218 + (x % 18), x + 12, 220 + (x % 18)), fill=self._mix(water, (81, 95, 150), 0.45))

    def _bridge(self, draw: ImageDraw.ImageDraw, palette: dict[str, str]) -> None:
        bridge = self._mix(self._hex(palette["accent"]), (240, 210, 160), 0.45)
        dark = (26, 25, 53)
        draw.line((25, 178, 190, 174), fill=bridge, width=2)
        draw.line((25, 184, 190, 180), fill=dark, width=3)
        draw.rectangle((56, 135, 60, 186), fill=bridge)
        draw.rectangle((138, 126, 143, 182), fill=bridge)
        draw.arc((55, 130, 143, 210), 190, 350, fill=bridge, width=2)
        for x in range(64, 140, 10):
            draw.line((x, 147, x + 4, 181), fill=bridge)

    def _city(self, draw: ImageDraw.ImageDraw, state: str, palette: dict[str, str]) -> None:
        body = (12, 17, 44) if state != "burnt" else (15, 9, 18)
        outline = (82, 58, 113) if state != "burnt" else (87, 28, 32)
        buildings = [
            (172, 125, 14, 60), (192, 108, 19, 80), (216, 134, 16, 51), (240, 112, 18, 76),
            (265, 86, 22, 102), (292, 112, 16, 75), (313, 72, 18, 118), (337, 52, 22, 142),
            (366, 96, 18, 92), (390, 120, 15, 66), (416, 78, 20, 109), (443, 110, 14, 76),
        ]
        for x, y, w, h in buildings:
            if state == "burnt":
                collapse = (x + h) % 21
                jag = [(x, y + collapse % 10), (x + w // 3, y + 7), (x + w // 2, y - 4), (x + w, y + collapse % 14), (x + w, y + h), (x, y + h)]
                draw.polygon(jag, fill=body, outline=outline)
                if h > 72:
                    draw.line((x + 2, y + 18, x + w - 2, y + h - 8), fill=(255, 72, 35), width=1)
                    draw.line((x + w - 2, y + 26, x + 2, y + h - 16), fill=(116, 36, 34), width=1)
            else:
                draw.rectangle((x, y, x + w, y + h), fill=body, outline=outline)
            if h > 90:
                draw.rectangle((x + w // 2, y - 13, x + w // 2 + 2, y), fill=outline)
            self._windows(draw, x, y, w, h, state, palette)
        draw.rectangle((167, 184, 466, 192), fill=(18, 18, 43))

    def _windows(self, draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, state: str, palette: dict[str, str]) -> None:
        if state == "burnt":
            on_every = 1
        elif state == "inferno":
            on_every = 2
        else:
            on_every = 4
        color = self._hex(palette["window"])
        dark = (25, 31, 63)
        idx = 0
        for yy in range(y + 7, y + h - 5, 9):
            for xx in range(x + 4, x + w - 3, 6):
                fill = color if idx % on_every == 0 or state in {"burning", "inferno", "burnt"} and idx % 3 == 0 else dark
                draw.rectangle((xx, yy, xx + 2, yy + 3), fill=fill)
                idx += 1

    def _domes(self, draw: ImageDraw.ImageDraw, state: str, palette: dict[str, str]) -> None:
        dome = self._mix(self._hex(palette["accent"]), (255, 218, 163), 0.38)
        shadow = (20, 20, 50)
        for cx, cy, r in [(72, 224, 31), (382, 215, 24), (430, 205, 20)]:
            draw.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=dome, outline=shadow)
            draw.rectangle((cx - r, cy, cx + r, cy + 13), fill=shadow, outline=dome)
            for dx in range(-r + 6, r, 10):
                draw.line((cx + dx, cy - 2, cx + dx + 5, cy - r + 8), fill=shadow)
        if state in {"burning", "inferno"}:
            draw.rectangle((428, 185, 438, 199), fill=self._hex(palette["window"]))

    def _foreground(self, draw: ImageDraw.ImageDraw, state: str, palette: dict[str, str]) -> None:
        ground = (9, 18, 34) if state != "burnt" else (20, 7, 10)
        draw.polygon([(0, 246), (60, 236), (152, 250), (260, 238), (342, 250), (512, 229), (512, 288), (0, 288)], fill=ground)
        foliage = {
            "alive": (42, 101, 76),
            "warming": (103, 84, 50),
            "burning": (82, 53, 46),
            "inferno": (42, 24, 28),
            "burnt": (64, 18, 19),
            "recovering": (54, 131, 91),
        }[state]
        purple = (89, 45, 120) if state != "burnt" else (92, 24, 29)
        for x, y, r, color in [(8, 246, 22, foliage), (42, 236, 17, purple), (458, 232, 26, purple), (492, 220, 22, foliage), (218, 246, 20, foliage)]:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
            draw.rectangle((x - 3, y, x + 3, 286), fill=(20, 18, 34))

    def _state_overlays(self, draw: ImageDraw.ImageDraw, state: str, palette: dict[str, str]) -> None:
        fire = self._hex(palette["window"])
        if state == "warming":
            for x, y, w, h in [(278, 70, 22, 62), (332, 48, 28, 78), (402, 82, 24, 56)]:
                smoke = (18, 13, 17)
                for step in range(0, h, 9):
                    offset = (step // 9 % 3) * 3 - 3
                    draw.rectangle((x + offset, y + step, x + w + offset, y + step + 7), fill=smoke)
                draw.rectangle((x + 3, y - 6, x + w - 5, y + 4), fill=(9, 7, 10))
        if state in {"burning", "inferno", "burnt"}:
            fire_points = [(278, 128, 9), (343, 102, 13), (424, 130, 11), (392, 166, 7)]
            if state == "burnt":
                fire_points.extend([(184, 148, 8), (242, 118, 12), (315, 94, 15), (362, 76, 17), (452, 136, 12), (72, 228, 10), (430, 203, 12)])
            for x, y, s in fire_points:
                draw.polygon([(x, y + s), (x + s // 2, y - s), (x + s, y + s)], fill=fire)
                draw.polygon([(x + 2, y + s), (x + s // 2, y - s // 2), (x + s - 2, y + s)], fill=(255, 216, 80))
        if state in {"inferno", "burnt"}:
            draw.rectangle((0, 191, 512, 288), fill=(30, 9, 16) if state == "inferno" else (22, 5, 8))
            for x in range(0, 512, 8):
                if x % 24:
                    draw.rectangle((x, 248 - x % 31, x + 2, 250 - x % 31), fill=(255, 82, 40))
        if state == "recovering":
            for x in range(0, 512, 13):
                draw.line((x, 0, x - 12, 68), fill=(82, 186, 218), width=1)
        if state == "burnt":
            for x in range(0, 512, 11):
                y = 108 + x % 124
                draw.rectangle((x, y, x + 2, y + 2), fill=(255, 96, 44))
            for x in range(172, 470, 28):
                y = 178 + x % 36
                draw.polygon([(x, y + 24), (x + 9, y - 18), (x + 19, y + 24)], fill=(255, 62, 28))
                draw.polygon([(x + 4, y + 22), (x + 10, y - 6), (x + 15, y + 22)], fill=(255, 210, 70))
            for x, y, w, h in [(188, 164, 28, 20), (250, 150, 44, 16), (330, 140, 36, 22), (404, 168, 52, 18)]:
                draw.polygon([(x, y), (x + w, y + 4), (x + w - 8, y + h), (x + 5, y + h - 2)], fill=(42, 10, 14), outline=(255, 67, 34))
            for box in [(42, 174, 76, 190), (97, 168, 128, 187), (145, 172, 186, 189)]:
                draw.rectangle(box, fill=(16, 5, 8))
            draw.line((26, 179, 65, 190), fill=(255, 87, 40), width=1)
            draw.line((96, 186, 138, 171), fill=(255, 87, 40), width=1)
            draw.polygon([(103, 82), (157, 81), (151, 111), (110, 122)], fill=(28, 6, 10))
            draw.rectangle((96, 98, 162, 106), fill=(255, 84, 37))
            draw.rectangle((111, 118, 151, 124), fill=(255, 117, 45))
            for x in range(0, 512, 18):
                draw.rectangle((x, 238 + x % 28, x + 10, 241 + x % 28), fill=(62, 13, 15))

    def _dither_pixels(self, draw: ImageDraw.ImageDraw, state: str, rng: random.Random) -> None:
        colors = {
            "alive": [(255, 134, 92), (80, 60, 140), (42, 200, 240)],
            "warming": [(255, 111, 60), (163, 57, 84), (230, 151, 66)],
            "burning": [(255, 75, 47), (95, 20, 40), (255, 190, 70)],
            "inferno": [(255, 42, 26), (70, 10, 25), (255, 120, 50)],
            "burnt": [(255, 68, 34), (156, 30, 26), (46, 10, 14), (255, 183, 58)],
            "recovering": [(72, 168, 146), (65, 126, 156), (128, 230, 178)],
        }[state]
        for _ in range(950):
            x = rng.randrange(0, 512)
            y = rng.randrange(28, 286)
            draw.point((x, y), fill=rng.choice(colors))

    def _clouds(self, directory: Path) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        paths = []
        specs = [(84, 34), (72, 28), (96, 38)]
        for idx, (w, h) in enumerate(specs, start=1):
            img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            color = (158, 96, 178, 190)
            for x, y, r in [(14, 19, 11), (29, 13, 15), (48, 17, 13), (64, 21, 10)]:
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
            draw.rectangle((9, 18, w - 9, h - 7), fill=color)
            path = directory / f"cloud_{idx:02d}.png"
            img.save(path)
            paths.append(path)
        return paths

    def _smoke(self, directory: Path) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        paths = []
        for name, color in [("smoke_light_01.png", (104, 91, 116, 150)), ("smoke_heavy_01.png", (38, 31, 43, 185))]:
            img = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            for box in [(8, 30, 38, 60), (25, 18, 58, 52), (36, 30, 68, 64), (17, 8, 44, 35)]:
                draw.ellipse(box, fill=color)
            path = directory / name
            img.save(path)
            paths.append(path)
        return paths

    def _fire(self, directory: Path) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        paths = []
        for name, size in [("fire_small_01.png", 36), ("fire_roof_01.png", 52), ("fire_large_01.png", 72)]:
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon([(size * 0.15, size * 0.9), (size * 0.5, size * 0.05), (size * 0.85, size * 0.9)], fill=(238, 64, 45, 240))
            draw.polygon([(size * 0.28, size * 0.9), (size * 0.55, size * 0.25), (size * 0.75, size * 0.9)], fill=(255, 143, 48, 250))
            draw.polygon([(size * 0.4, size * 0.9), (size * 0.55, size * 0.45), (size * 0.65, size * 0.9)], fill=(255, 227, 90, 255))
            path = directory / name
            img.save(path)
            paths.append(path)
        return paths

    def _particles(self, directory: Path) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        specs = {
            "ember_01.png": ((16, 16), (255, 114, 45, 255), [(7, 7, 10, 10), (5, 8, 12, 9)]),
            "ash_01.png": ((12, 12), (162, 154, 150, 190), [(5, 5, 7, 7)]),
            "rain_streak_01.png": ((8, 28), (93, 194, 232, 170), [(3, 0, 4, 27), (4, 1, 5, 27)]),
        }
        paths = []
        for name, (size, color, rects) in specs.items():
            img = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            for rect in rects:
                draw.rectangle(rect, fill=color)
            path = directory / name
            img.save(path)
            paths.append(path)
        return paths

    def _birds(self, directory: Path) -> list[Path]:
        directory.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGBA", (32, 18), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.line((3, 10, 12, 5, 16, 9, 20, 5, 29, 10), fill=(10, 10, 18, 230), width=3)
        path = directory / "bird_01.png"
        img.save(path)
        return [path]

    def _hex(self, value: str) -> tuple[int, int, int]:
        value = value.lstrip("#")
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))

    def _mix(self, a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
        return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
