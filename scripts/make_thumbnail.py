#!/usr/bin/env python3
"""1280x720 유튜브 썸네일 시안 렌더러.

사용 예:
  python3 scripts/make_thumbnail.py --text "PG 심사|또 반려?" --brand vibepay \
      --badge "반려 사유 TOP 7" --out episodes/vibepay/<id>/thumbnail_A.png [--bg bg.png]

- --text: '|'로 줄바꿈 (최대 2줄 권장). 두 번째 줄은 강조색으로 렌더
- --font: 한글 굵은 폰트 경로 (Pretendard-ExtraBold.otf 등 권장). 미지정 시 FONT_PATH 환경변수 → 시스템 한글 폰트
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720

BRANDS = {
    # 임시 컬러 — brands/*.md §7 확정 후 교체
    "vibepay": {"bg1": (17, 24, 39), "bg2": (124, 58, 237), "text": (255, 255, 255), "accent": (250, 204, 21)},
    "moduplay": {"bg1": (20, 83, 45), "bg2": (22, 163, 74), "text": (255, 255, 255), "accent": (249, 115, 22)},
}

FALLBACK_FONTS = [
    "/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgunbd.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]


def find_font(path):
    for p in [path, os.environ.get("FONT_PATH")] + FALLBACK_FONTS:
        if p and os.path.exists(p):
            return p
    sys.exit("한글 폰트를 찾을 수 없습니다. --font 로 경로를 지정하세요.")


def gradient(c1, c2):
    img = Image.new("RGB", (W, H), c1)
    d = ImageDraw.Draw(img)
    for x in range(W):
        t = x / (W - 1)
        d.line([(x, 0), (x, H)], fill=tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)))
    return img


def fit_size(draw, lines, font_path, max_w, max_h):
    size = 220
    while size > 40:
        f = ImageFont.truetype(font_path, size)
        widths = [draw.textbbox((0, 0), ln, font=f, stroke_width=size // 14)[2] for ln in lines]
        if max(widths) <= max_w and size * 1.15 * len(lines) <= max_h:
            return f
        size -= 6
    return ImageFont.truetype(font_path, size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--brand", choices=BRANDS, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bg", help="배경 이미지 (선택)")
    ap.add_argument("--badge", help="좌상단 작은 라벨 (선택)")
    ap.add_argument("--font")
    a = ap.parse_args()

    c = BRANDS[a.brand]
    font_path = find_font(a.font)

    if a.bg:
        img = Image.open(a.bg).convert("RGB")
        scale = max(W / img.width, H / img.height)
        img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1))
        left, top = (img.width - W) // 2, (img.height - H) // 2
        img = img.crop((left, top, left + W, top + H))
        # 텍스트 가독성용 좌측 어둡게
        shade = Image.new("L", (W, H))
        ImageDraw.Draw(shade).rectangle([0, 0, W, H], fill=0)
        for x in range(W):
            ImageDraw.Draw(shade).line([(x, 0), (x, H)], fill=int(170 * max(0, 1 - x / (W * 0.75))))
        img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shade)
    else:
        img = gradient(c["bg1"], c["bg2"])

    draw = ImageDraw.Draw(img)
    lines = [ln.strip() for ln in a.text.split("|") if ln.strip()]
    font = fit_size(draw, lines, font_path, int(W * 0.86), int(H * 0.62))
    sw = max(4, font.size // 14)
    lh = int(font.size * 1.15)
    y = (H - lh * len(lines)) // 2 + (40 if a.badge else 0)

    # 그림자 레이어
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, ln in enumerate(lines):
        sd.text((70 + 8, y + i * lh + 8), ln, font=font, fill=(0, 0, 0, 180))
    img.paste(shadow.filter(ImageFilter.GaussianBlur(8)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(8)))

    for i, ln in enumerate(lines):
        fill = c["accent"] if (i == len(lines) - 1 and len(lines) > 1) else c["text"]
        draw.text((70, y + i * lh), ln, font=font, fill=fill, stroke_width=sw, stroke_fill=(0, 0, 0))

    if a.badge:
        bf = ImageFont.truetype(font_path, 44)
        bw = draw.textbbox((0, 0), a.badge, font=bf)[2]
        draw.rounded_rectangle([60, 50, 60 + bw + 48, 50 + 76], radius=18, fill=c["accent"])
        draw.text((84, 62), a.badge, font=bf, fill=(0, 0, 0))

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    img.save(a.out, optimize=True)
    kb = os.path.getsize(a.out) / 1024
    print(f"saved {a.out} ({W}x{H}, {kb:.0f}KB, font={os.path.basename(font_path)})")
    if kb > 2048:
        print("경고: 2MB 초과 — JPG로 저장하세요 (--out *.jpg)")


if __name__ == "__main__":
    main()
