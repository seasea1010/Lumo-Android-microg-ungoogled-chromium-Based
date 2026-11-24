#!/usr/bin/env python3
"""Generate the Android launcher icons in misc/app_icons/ from the decided
square Lumo icon (navy square + single cyan L, no glow/gradient/gloss).

- app_icon.png: the square composition resized as-is.
- layered_app_icon_background.png: solid navy.
- layered_app_icon.png: the L extracted (alpha = fraction along navy->cyan),
  forced to the flat cyan, placed at 90% scale centered for adaptive-icon
  safe zones.

Usage: generate-icons.py <path-to-lumo-icon-square-1600.png> <repo-root>
"""
import os
import sys

import numpy as np
from PIL import Image

NAVY = np.array([25, 29, 73], dtype=float)
CYAN = np.array([0, 168, 222], dtype=float)

SIZES = {  # density: (app_icon px, layered px)
    "mipmap-mdpi": (48, 108),
    "mipmap-hdpi": (72, 162),
    "mipmap-xhdpi": (96, 216),
    "mipmap-xxhdpi": (144, 324),
    "mipmap-xxxhdpi": (192, 432),
}


def main() -> None:
    src_path, repo_root = sys.argv[1], sys.argv[2]
    base = os.path.join(repo_root, "misc", "app_icons")

    src = Image.open(src_path).convert("RGB")
    a = np.array(src).astype(float)

    v = CYAN - NAVY
    frac = np.clip(((a - NAVY) @ v) / (v * v).sum(), 0, 1)
    fg = np.zeros((a.shape[0], a.shape[1], 4), dtype=np.uint8)
    fg[:, :, 0:3] = CYAN.astype(np.uint8)
    fg[:, :, 3] = (frac * 255).round().astype(np.uint8)
    fg_img = Image.fromarray(fg, "RGBA")

    for density, (app_sz, lay_sz) in SIZES.items():
        out = os.path.join(base, density)
        src.resize((app_sz, app_sz), Image.LANCZOS).save(f"{out}/app_icon.png")
        Image.new("RGB", (lay_sz, lay_sz), (25, 29, 73)).save(
            f"{out}/layered_app_icon_background.png"
        )
        inner_sz = int(lay_sz * 0.9)
        inner = fg_img.resize((inner_sz, inner_sz), Image.LANCZOS)
        canvas = Image.new("RGBA", (lay_sz, lay_sz), (0, 0, 0, 0))
        off = (lay_sz - inner_sz) // 2
        canvas.paste(inner, (off, off), inner)
        canvas.save(f"{out}/layered_app_icon.png")
        print(density, "done")


if __name__ == "__main__":
    main()
