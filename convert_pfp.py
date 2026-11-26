"""Convert a profile image to colored ASCII: python convert_pfp.py path/to/image.jpg.

Requires Pillow only when converting a new image; the scheduled updater uses
the generated JSON with Python's standard library.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageOps


def convert(image_path):
    with Image.open(image_path) as source:
        # Characters are half as wide as they are tall. Resize the entire image
        # to the character grid; fitting to this 2:1 grid would crop a square PFP.
        portrait = ImageOps.exif_transpose(source).convert("RGB").resize(
            (72, 36), Image.Resampling.LANCZOS
        )
    ramp = "oxkO0XNW"
    rows = []
    for y in range(portrait.height):
        spans = []
        for x in range(portrait.width):
            r, g, b = portrait.getpixel((x, y))
            luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
            char = ramp[round(luminance * (len(ramp) - 1))]
            color = f"#{r:02x}{g:02x}{b:02x}"
            if spans and spans[-1][1] == color:
                spans[-1][0] += char
            else:
                spans.append([char, color])
        rows.append(spans)
    Path(__file__).with_name("pfp_data.json").write_text(
        json.dumps(rows, separators=(",", ":")) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    convert(sys.argv[1])
