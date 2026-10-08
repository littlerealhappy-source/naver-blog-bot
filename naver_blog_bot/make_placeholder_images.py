# -*- coding: utf-8 -*-
"""
자리표시 사진 생성. 원고의 [권장 사진] 지시를 넣어둘 용도이고,
발행 전에 실제 사진으로 교체한다.

사용법:
    python make_placeholder_images.py <접두어> <장수> ["설명1" "설명2" ...]

예:
    python make_placeholder_images.py knee 5
    python make_placeholder_images.py knee 2 "계단에서 무릎을 짚는 모습" "무릎 관절 구조 그림"

설명을 주면 사진 안에 함께 그린다. 줄바꿈은 \\n 으로 넣는다.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "stock_images"
SIZE = (1200, 700)
PALETTE = ["#6E7F9B", "#8A6A8C", "#5E8A74", "#96774E", "#5B86A0", "#9C6B6B"]

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgun.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
]
FONT_BOLD_CANDIDATES = [r"C:\Windows\Fonts\malgunbd.ttf"] + FONT_CANDIDATES


def load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_centered(draw, text, font, center_x, top):
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((center_x - (bbox[2] - bbox[0]) / 2, top), text, font=font, fill="white")


def make_image(path: Path, bg_hex: str, title: str, desc: str) -> None:
    img = Image.new("RGB", SIZE, bg_hex)
    draw = ImageDraw.Draw(img)
    title_font = load_font(FONT_BOLD_CANDIDATES, 64)
    desc_font = load_font(FONT_CANDIDATES, 34)

    draw_centered(draw, title, title_font, SIZE[0] / 2, SIZE[1] / 2 - 100)
    for i, line in enumerate(desc.split("\n")):
        if line:
            draw_centered(draw, line, desc_font, SIZE[0] / 2, SIZE[1] / 2 + 10 + i * 46)

    img.save(path, quality=90)
    print(f"생성: {path.name}")


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1

    prefix, count = argv[1], int(argv[2])
    descs = argv[3:]

    OUT_DIR.mkdir(exist_ok=True)
    for i in range(1, count + 1):
        desc = descs[i - 1].replace("\\n", "\n") if i <= len(descs) else ""
        make_image(
            OUT_DIR / f"{prefix}_{i:02d}.jpg",
            PALETTE[(i - 1) % len(PALETTE)],
            f"사진 자리 {i}",
            desc,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
