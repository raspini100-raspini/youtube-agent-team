#!/usr/bin/env python3
"""모두플레이 오픈일 쇼츠 렌더러 (모션그래픽 + 자막, 내레이션 없음).

episodes/moduplay/20261110-launch-short/shorts.md 의 B안 훅 버전을 1080x1920 30fps MP4로 만든다.
등장 화면은 모두 이해를 돕는 자체 예시 목업이며 실제 앱 화면이 아니다 (화면에 '예시 화면' 표기).

사용: python3 scripts/render_launch_short.py [--out episodes/moduplay/20261110-launch-short/short.mp4] [--preview 12.5]
"""
import argparse
import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "assets", "fonts")
W, H, FPS = 1080, 1920, 30
DUR = 40.0

GREEN = (23, 61, 53)
GREEN2 = (32, 84, 73)
MINT = (232, 241, 238)
CREAM = (250, 247, 240)
ORANGE = (249, 115, 22)
WHITE = (255, 255, 255)
INK = (24, 32, 30)
GREY = (120, 132, 128)
RED = (220, 60, 50)
OK = (22, 140, 90)

_fc = {}


def font(size, weight="ExtraBold"):
    k = (size, weight)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONT, f"Pretendard-{weight}.otf"), size)
    return _fc[k]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def prog(t, start, dur=0.35):
    return ease((t - start) / dur)


def text_c(d, cx, y, s, f, fill, alpha=1.0, bg=None):
    """가운데 정렬 텍스트. alpha<1이면 배경색과 섞어 페이드."""
    if bg is not None and alpha < 1:
        fill = tuple(int(b + (c - b) * alpha) for c, b in zip(fill, bg))
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)


def caption(d, t, start, lines, bg, color=WHITE, hl=None, y=250, size=84):
    """상단 자막(쇼츠 UI가 가리지 않는 위치). hl: 강조할 단어 → 오렌지."""
    a = prog(t, start, 0.25)
    dy = int((1 - a) * 40)
    for i, ln in enumerate(lines):
        f = font(size)
        if hl and hl in ln:
            pre, post = ln.split(hl, 1)
            total = d.textlength(ln, font=f)
            x = W / 2 - total / 2
            yy = y + i * int(size * 1.25) + dy
            for part, col in ((pre, color), (hl, ORANGE), (post, color)):
                c = tuple(int(b + (cc - b) * a) for cc, b in zip(col, bg))
                d.text((x, yy), part, font=f, fill=c)
                x += d.textlength(part, font=f)
        else:
            text_c(d, W / 2, y + i * int(size * 1.25) + dy, ln, f, color, a, bg)


def brand_tag(d, bg):
    f = font(34, "Bold")
    d.rounded_rectangle([60, 110, 60 + d.textlength("모두플레이", font=f) + 48, 170], radius=30,
                        fill=GREEN if bg != GREEN else GREEN2)
    d.text((84, 118), "모두플레이", font=f, fill=WHITE)


def example_label(d):
    f = font(28, "Medium")
    s = "이해를 돕는 예시 화면"
    w = d.textlength(s, font=f)
    d.rounded_rectangle([W / 2 - w / 2 - 20, 1430, W / 2 + w / 2 + 20, 1478], radius=24, fill=(0, 0, 0, 0), outline=GREY, width=2)
    d.text((W / 2 - w / 2, 1437), s, font=f, fill=GREY)


def card(d, box, fill=WHITE, r=36, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        d.rounded_rectangle([x0 + 8, y0 + 14, x1 + 8, y1 + 14], radius=r, fill=(0, 0, 0, 40))
    d.rounded_rectangle(box, radius=r, fill=fill)


# ---------------- scenes ----------------
def s_hook(img, d, t):  # 0–3 단톡 미납 공지
    bg = GREEN
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 0.0 - 1, ["회비 안 낸 사람,", "또 단톡에 물어보셨죠?"], bg, hl="회비", y=260, size=92)
    card(d, [120, 640, 960, 1380], fill=MINT)
    d.text((170, 680), "우리 모임 단톡", font=font(40, "Bold"), fill=INK)
    for i in range(3):
        a = 1.0 if i == 0 else prog(t, i * 0.8, 0.3)
        if a <= 0:
            continue
        y = 800 + i * 170 + int((1 - a) * 30)
        d.rounded_rectangle([370, y, 920, y + 120], radius=40, fill=(255, 236, 214))
        d.text((410, y + 34), "회비 아직 안 내신 분~", font=font(44, "Bold"), fill=INK)
        d.text((260, y + 70), f"읽음 {14 - i * 3}", font=font(28, "Medium"), fill=GREY)
    if t > 2.2:
        text_c(d, W / 2, 1300, "벌써 세 번째 공지", font(40, "Bold"), RED)
    brand_tag(d, bg)


def s_bank(img, d, t):  # 3–6 입금자명
    bg = CREAM
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 3.0, ["'민수엄마'는", "누구죠?"], bg, color=INK, hl="민수엄마", size=96)
    card(d, [110, 620, 970, 1360])
    d.text((160, 660), "입금 내역", font=font(44, "Bold"), fill=INK)
    rows = [("민수엄마", "30,000"), ("ㄱㅁㅅ", "30,000"), ("회비요", "30,000"), ("김", "15,000")]
    for i, (n, amt) in enumerate(rows):
        a = prog(t, 3.2 + i * 0.25, 0.3)
        y = 770 + i * 140
        col = tuple(int(255 + (c - 255) * a) for c in INK)
        if i == 0 and t > 4.2:
            d.rounded_rectangle([140, y - 18, 940, y + 92], radius=24, fill=(255, 236, 214))
        d.text((180, y), n, font=font(54, "Bold"), fill=col)
        w = d.textlength(amt + "원", font=font(50, "Bold"))
        d.text((900 - w, y + 4), amt + "원", font=font(50, "Bold"), fill=col)
        if i < 3:
            d.line([170, y + 112, 910, y + 112], fill=(230, 230, 226), width=2)
    if t > 4.6:
        text_c(d, W / 2 - 160, 860, "?", font(110), ORANGE)
    brand_tag(d, bg)


def s_excel(img, d, t):  # 6–9 밤 11시 장부
    bg = (20, 28, 34)
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 6.0, ["장부 정리는", "밤 11시"], bg, hl="밤 11시", size=100)
    card(d, [100, 640, 980, 1320], fill=(244, 246, 245), r=24, shadow=False)
    cols = [100, 330, 560, 780, 980]
    for r in range(8):
        y = 640 + r * 85
        d.line([100, y, 980, y], fill=(200, 205, 203), width=2)
    for x in cols:
        d.line([x, 640, x, 1320], fill=(200, 205, 203), width=2)
    heads = ["이름", "9월", "10월", "11월"]
    for i, h in enumerate(heads):
        d.text((cols[i] + 24, 660), h, font=font(36, "Bold"), fill=INK)
    marks = [["회원 A", "완납", "완납", "미납"], ["회원 B", "완납", "미납", "미납"], ["회원 C", "완납", "완납", "?"],
             ["회원 D", "미납", "완납", "?"], ["회원 E", "완납", "?", "?"]]
    n = int(min(len(marks), max(0, (t - 6.2) / 0.35)))
    for r, row in enumerate(marks[:n]):
        for i, v in enumerate(row):
            c = INK if i == 0 else (OK if v == "완납" else RED if v == "미납" else GREY)
            d.text((cols[i] + 24, 745 + r * 85), v, font=font(36, "Bold"), fill=c)
    # 시계
    cx, cy, rr = 860, 1470, 70
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=WHITE, width=6)
    d.line([cx, cy, cx, cy - 50], fill=WHITE, width=6)
    ang = -math.pi / 2 - math.pi / 6
    d.line([cx, cy, cx + 38 * math.cos(ang), cy + 38 * math.sin(ang)], fill=ORANGE, width=8)
    d.text((140, 1440), "23:00", font=font(64), fill=WHITE)


def s_thanks(img, d, t):  # 9–11
    bg = ORANGE
    d.rectangle([0, 0, W, H], fill=bg)
    a = prog(t, 9.0, 0.4)
    text_c(d, W / 2, 760, "총무님,", font(120), WHITE, a, bg)
    text_c(d, W / 2, 920, "고생 많으셨습니다", font(110), WHITE, a, bg)


def s_open(img, d, t):  # 11–15
    bg = GREEN
    d.rectangle([0, 0, W, H], fill=bg)
    a = prog(t, 11.0, 0.5)
    s = 0.85 + 0.15 * a
    text_c(d, W / 2, 330, "모두플레이", font(int(70 * s), "Bold"), MINT, a, bg)
    text_c(d, W / 2, 560, "11.10", font(int(260 * s), "Black"), ORANGE, a, bg)
    text_c(d, W / 2, 860, "카드결제 OPEN", font(int(130 * s), "Black"), WHITE, a, bg)
    b = prog(t, 12.2, 0.4)
    text_c(d, W / 2, 1120, "11월 10일, 카드결제 오픈", font(64, "Bold"), MINT, b, bg)


def phone(d, x0, y0, w=560, h=1000):
    d.rounded_rectangle([x0 - 14, y0 - 14, x0 + w + 14, y0 + h + 14], radius=70, fill=INK)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=58, fill=WHITE)


def s_pay(img, d, t):  # 15–18
    bg = MINT
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 15.0, ["회원은 카드로", "회비 결제"], bg, color=INK, hl="카드로", size=96)
    x0, y0 = 260, 560
    phone(d, x0, y0, 560, 840)
    d.text((x0 + 50, y0 + 70), "11월 정모 회비", font=font(46, "Bold"), fill=INK)
    d.text((x0 + 50, y0 + 150), "30,000원", font=font(84), fill=INK)
    d.text((x0 + 50, y0 + 270), "결제수단", font=font(34, "Medium"), fill=GREY)
    d.rounded_rectangle([x0 + 50, y0 + 320, x0 + 510, y0 + 420], radius=20, outline=GREEN, width=4)
    d.text((x0 + 80, y0 + 345), "신용·체크카드", font=font(40, "Bold"), fill=GREEN)
    press = 1 - 0.06 * math.sin(min(1, max(0, (t - 16.6) / 0.3)) * math.pi)
    bw, bh = 460 * press, 120 * press
    bx, by = x0 + 280 - bw / 2, y0 + 650 - bh / 2
    done = t > 17.0
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=30, fill=OK if done else GREEN)
    text_c(d, x0 + 280, by + bh / 2 - 30, "결제 완료" if done else "카드로 결제", font(48, "Bold"), WHITE)
    example_label(d)


def s_ledger(img, d, t):  # 18–22
    bg = MINT
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 18.0, ["누가 냈는지", "회비 장부에"], bg, color=INK, hl="회비 장부", size=96)
    card(d, [110, 600, 970, 1400])
    d.text((160, 640), "회비 장부 · 11월", font=font(46, "Bold"), fill=INK)
    rows = [("회원 A", True), ("회원 B", True), ("회원 C", False), ("회원 D", True), ("회원 E", False)]
    for i, (n, paid) in enumerate(rows):
        a = prog(t, 18.3 + i * 0.3, 0.3)
        if a <= 0:
            continue
        y = 750 + i * 125
        d.text((170, y + int((1 - a) * 20)), n, font=font(48, "Bold"), fill=INK)
        d.text((480, y + 4), "30,000원", font=font(44, "Medium"), fill=GREY)
        chip = "완납" if paid else "미납"
        c = OK if paid else RED
        d.rounded_rectangle([760, y - 6, 910, y + 62], radius=34, fill=c)
        text_c(d, 835, y + 2, chip, font(38, "Bold"), WHITE)
    example_label(d)


def s_split(img, d, t):  # 22–26
    bg = CREAM
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 22.0, ["정모비 엔빵은", "1/N 기능으로"], bg, color=INK, hl="1/N", size=96)
    card(d, [110, 620, 970, 1380])
    d.text((160, 660), "1/N 정산", font=font(46, "Bold"), fill=INK)
    d.text((160, 760), "코트비 + 음료", font=font(40, "Medium"), fill=GREY)
    d.text((160, 820), "120,000원", font=font(96), fill=INK)
    a = prog(t, 23.0, 0.4)
    text_c(d, W / 2, 1000, "÷ 8명", font(84), ORANGE, a, WHITE)
    b = prog(t, 23.8, 0.4)
    text_c(d, W / 2, 1150, "1인 15,000원", font(100), GREEN, b, WHITE)
    example_label(d)


def s_fee(img, d, t):  # 26–31
    bg = WHITE
    d.rectangle([0, 0, W, H], fill=bg)
    a = prog(t, 26.0, 0.4)
    text_c(d, W / 2, 230, "카드수수료", font(80, "Bold"), INK, a, bg)
    text_c(d, W / 2, 360, "4.4%", font(300, "Black"), ORANGE, a, bg)
    b = prog(t, 26.6, 0.4)
    text_c(d, W / 2, 760, "결제하는 회원이 부담", font(96), INK, b, bg)
    c = prog(t, 27.6, 0.4)
    d.rounded_rectangle([170, 980, 910, 1110], radius=65, fill=tuple(int(255 + (m - 255) * c) for m in MINT))
    text_c(d, W / 2, 1012, "모임은 카드수수료 부담 없음", font(52, "Bold"), GREEN, c, MINT)


def s_notice(img, d, t):  # 31–34
    bg = GREEN
    d.rectangle([0, 0, W, H], fill=bg)
    caption(d, t, 31.0, ["회원들께", "미리 공지해 주세요"], bg, hl="미리 공지", size=92)
    card(d, [120, 680, 960, 1240], fill=MINT)
    d.text((170, 720), "우리 모임 단톡", font=font(40, "Bold"), fill=INK)
    a = prog(t, 31.6, 0.35)
    if a > 0:
        y = 860 + int((1 - a) * 30)
        d.rounded_rectangle([200, y, 920, y + 260], radius=40, fill=WHITE)
        d.text((240, y + 40), "[공지] 다음 달부터 회비는", font=font(44, "Bold"), fill=INK)
        d.text((240, y + 105), "모두플레이 카드결제로 받아요.", font=font(44, "Bold"), fill=INK)
        d.text((240, y + 170), "카드수수료 4.4%는 결제자 부담", font=font(38, "Medium"), fill=GREY)
    brand_tag(d, bg)


def s_settle(img, d, t):  # 34–37
    bg = CREAM
    d.rectangle([0, 0, W, H], fill=bg)
    a = prog(t, 34.0, 0.4)
    text_c(d, W / 2, 300, "정산은", font(90, "Bold"), INK, a, bg)
    text_c(d, W / 2, 420, "D+1", font(260, "Black"), GREEN, a, bg)
    for i, (lbl, sub) in enumerate((("결제일", "D"), ("다음 날", "D+1"))):
        b = prog(t, 34.6 + i * 0.5, 0.35)
        x = 170 + i * 420
        col = tuple(int(255 + (c - 255) * b) for c in (GREEN if i else INK))
        d.rounded_rectangle([x, 900, x + 320, 1200], radius=36, outline=col, width=6)
        text_c(d, x + 160, 950, lbl, font(48, "Bold"), col)
        text_c(d, x + 160, 1040, sub, font(90), col)
    if t > 35.4:
        d.line([500, 1050, 545, 1050], fill=ORANGE, width=10)
        d.polygon([(575, 1050), (540, 1028), (540, 1072)], fill=ORANGE)


def s_end(img, d, t):  # 37–40
    bg = GREEN
    d.rectangle([0, 0, W, H], fill=bg)
    a = prog(t, 37.0, 0.4)
    text_c(d, W / 2, 380, "우리 모임 총무님", font(100), WHITE, a, bg)
    text_c(d, W / 2, 520, "태그하세요", font(130, "Black"), ORANGE, a, bg)
    b = prog(t, 37.8, 0.4)
    d.rounded_rectangle([210, 800, 870, 920], radius=60, fill=tuple(int(g + (m - g) * b) for g, m in zip(GREEN, MINT)))
    text_c(d, W / 2, 828, "링크는 설명란에", font(56, "Bold"), GREEN, b, MINT)
    text_c(d, W / 2, 1060, "모두플레이 · 11.10 카드결제 OPEN", font(44, "Bold"), MINT, b, bg)


SCENES = [(0, 3, s_hook), (3, 6, s_bank), (6, 9, s_excel), (9, 11, s_thanks), (11, 15, s_open),
          (15, 18, s_pay), (18, 22, s_ledger), (22, 26, s_split), (26, 31, s_fee), (31, 34, s_notice),
          (34, 37, s_settle), (37, 40, s_end)]


def frame(t):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img, "RGBA")
    for s, e, fn in SCENES:
        if s <= t < e or (fn is s_end and t >= e):
            fn(img, d, t)
            break
    return img


def make_audio(path, dur):
    """자체 합성 배경음 (저작권 문제 없음): 부드러운 코드 패드 + 장면 전환 효과음."""
    sr = 44100
    n = int(sr * dur)
    tt = np.arange(n) / sr
    chords = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
    out = np.zeros(n)
    seg = 2.5
    for i in range(int(dur / seg) + 1):
        s0, s1 = int(i * seg * sr), min(n, int((i + 1) * seg * sr))
        if s0 >= n:
            break
        x = tt[s0:s1] - i * seg
        env = np.minimum(1, x / 0.3) * np.minimum(1, (seg - x) / 0.4)
        for f in chords[i % 4]:
            out[s0:s1] += 0.05 * env * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x))
    beat = 60 / 100
    for k in range(int(dur / beat)):
        s0 = int(k * beat * sr)
        m = min(n - s0, int(0.12 * sr))
        x = np.arange(m) / sr
        out[s0:s0 + m] += 0.12 * np.sin(2 * np.pi * (90 - 300 * x) * x) * np.exp(-x * 30)
    for s, _, _ in SCENES[1:]:
        s0 = int(s * sr)
        m = min(n - s0, int(0.15 * sr))
        x = np.arange(m) / sr
        out[s0:s0 + m] += 0.08 * np.sin(2 * np.pi * 880 * x) * np.exp(-x * 25)
    fade = int(1.0 * sr)
    out[-fade:] *= np.linspace(1, 0, fade)
    out = out / max(1e-6, np.abs(out).max()) * 0.5
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "episodes/moduplay/20261110-launch-short/short.mp4"))
    ap.add_argument("--preview", type=float, nargs="*", help="이 시각(초)의 프레임만 PNG로 저장")
    a = ap.parse_args()
    if a.preview:
        for s in a.preview:
            p = os.path.splitext(a.out)[0] + f"_preview_{s:05.1f}.png"
            frame(s).save(p)
            print("saved", p)
        return
    wav = os.path.splitext(a.out)[0] + "_bgm.wav"
    make_audio(wav, DUR)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print("saved", a.out)


if __name__ == "__main__":
    main()
