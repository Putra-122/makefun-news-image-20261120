#!/usr/bin/env python3
"""news-image-20261120 — one image summing up Friday 20 November 2026.

A procedural broadsheet. Nothing on the page is a photo or a pasted asset:
every picture is drawn in code by a small scene registry, the page is laid
out by a declarative stack/column engine, and all text is set by a tiny
typesetter. Stdlib + Pillow only, no network, no randomness (a fixed seed
drives the few decorative details, so the output is byte-identical every run).

Layout (1024x1024): navy masthead naming the day, one full-bleed illustrated
hero for the day's biggest story (GTA VI), a row of three story cards, each
with its own drawn scene, then an "also today" ticker and a sources footer.

Output: 1024x1024 JPEG, written to $MAKEFUN_OUTPUT_DIR/entry.png (and a copy
beside this file when the directory is writable).
"""

import hashlib
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (247, 243, 234)
NAVY = (14, 27, 46)
NAVY_DARK = (9, 18, 32)
GOLD = (198, 154, 60)
INK = (22, 22, 22)
GREY = (96, 96, 96)
RED = (178, 34, 34)
KICK = (150, 40, 30)

DJV = "/usr/share/fonts/truetype/dejavu"


# ---------------------------------------------------------------- fonts
def load_fonts():
    """All type on the page; DejaVu ships with the system, no download."""
    return {
        "mast": ImageFont.truetype(f"{DJV}/DejaVuSerif-Bold.ttf", 40),
        "kick": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 18),
        "side": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 18),
        "hero": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 48),
        "sub": ImageFont.truetype(f"{DJV}/DejaVuSans.ttf", 21),
        "card_kick": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 16),
        "card_head": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 24),
        "card_dek": ImageFont.truetype(f"{DJV}/DejaVuSans.ttf", 16),
        "tick": ImageFont.truetype(f"{DJV}/DejaVuSans.ttf", 17),
        "tag": ImageFont.truetype(f"{DJV}/DejaVuSans-Bold.ttf", 17),
        "foot": ImageFont.truetype(f"{DJV}/DejaVuSans.ttf", 15),
    }


# ---------------------------------------------------------------- helpers
def vgrad(size, stops):
    """Vertical gradient image. stops = [(0..1, (r, g, b)), ...], sorted."""
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        if t <= stops[0][0]:
            px[0, y] = stops[0][1]
            continue
        if t >= stops[-1][0]:
            px[0, y] = stops[-1][1]
            continue
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                px[0, y] = tuple(round(c0[k] + (c1[k] - c0[k]) * f)
                                 for k in range(3))
                break
    return img.resize((w, h))


def stack(y, heights, gap=0):
    """Split a vertical span into (y0, y1) bands from a list of heights."""
    spans = []
    for h in heights:
        spans.append((y, y + h))
        y += h + gap
    return spans


def cols(x, widths, gap=0):
    """Split a horizontal span into (x0, x1) columns from a list of widths."""
    spans = []
    for w in widths:
        spans.append((x, x + w))
        x += w + gap
    return spans


class Typesetter:
    """Word-wrap + draw paragraphs on one ImageDraw, nothing else."""

    def __init__(self, draw):
        self.d = draw

    @staticmethod
    def wrap(text, font, max_w):
        lines, cur = [], ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if font.getlength(trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, text, font, fill, max_w, leading=None):
        """Draw a wrapped paragraph; returns the y just below it."""
        lh = leading or int(font.size * 1.22)
        for line in self.wrap(text, font, max_w):
            self.d.text((x, y), line, font=font, fill=fill)
            y += lh
        return y

    def centred(self, cx, y, text, font, fill):
        self.d.text((cx - font.getlength(text) / 2, y), text,
                    font=font, fill=fill)
        return y + int(font.size * 1.22)


# ---------------------------------------------------------------- scenes
# Each scene paints one drawn illustration into box (x0, y0, x1, y1) of the
# page. No external images anywhere; every shape is computed from the box.

NEON = [(125, 249, 255), (255, 113, 206), (255, 209, 102), (255, 255, 255)]


def paint_skyline(page, draw, box):
    """Vice City at dusk: gradient sky, low sun, two rows of towers with
    lit windows, and a strip of water catching the neon."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    horizon = y1 - int(bh * 0.11)
    sky = vgrad((bw, horizon - y0),
                [(0.0, (26, 11, 46)), (0.55, (123, 45, 139)),
                 (0.82, (255, 107, 157)), (1.0, (255, 170, 120))])
    page.paste(sky, (x0, y0))
    # low sun with a solid stepped glow (no alpha needed); set high-left
    # in clear sky so no tower covers it
    sx, sy, sr = x0 + int(bw * 0.12), y0 + int(bh * 0.22), 38
    for r, col in ((88, (146, 62, 130)), (64, (214, 92, 140)),
                   (48, (255, 150, 130))):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 209, 102))
    # far towers, then nearer, taller ones in front of them
    rng = random.Random(20261120)
    far_h = [0.45, 0.60, 0.40, 0.65, 0.50, 0.58, 0.42, 0.55]
    slot = bw / len(far_h)
    for i, frac in enumerate(far_h):
        bx = x0 + int(i * slot) + 4
        bw_ = int(slot) - 8
        top = horizon - int((horizon - y0) * frac)
        draw.rectangle([bx, top, bx + bw_, horizon], fill=(43, 22, 64))
    near_h = [0.55, 0.75, 0.62, 0.82, 0.68]
    slot = bw / len(near_h)
    for i, frac in enumerate(near_h):
        bx = x0 + int(i * slot) + 6
        bw_ = int(slot) - 12
        top = horizon - int((horizon - y0) * frac)
        draw.rectangle([bx, top, bx + bw_, horizon], fill=(16, 8, 28))
        for wy in range(top + 12, horizon - 8, 22):
            for wx in range(bx + 8, bx + bw_ - 8, 16):
                if rng.random() < 0.30:
                    draw.rectangle([wx, wy, wx + 7, wy + 10],
                                   fill=rng.choice(NEON))
    # water strip with neon streaks
    draw.rectangle([x0, horizon, x1, y1], fill=(18, 10, 32))
    for _ in range(42):
        wx = rng.randint(x0, x1 - 70)
        wy = rng.randint(horizon + 4, y1 - 4)
        ln = rng.randint(15, 70)
        draw.line([(wx, wy), (wx + ln, wy)], fill=rng.choice(NEON), width=2)


def paint_tower(page, draw, box):
    """Riyadh at dusk: the Kingdom Centre slab with its open arch, a smoke
    plume above it, low blocks at its feet. The arch is left unpainted so
    the sky shows through it."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    page.paste(vgrad((bw, bh),
                     [(0.0, (58, 89, 130)), (0.65, (196, 138, 110)),
                      (1.0, (232, 164, 110))]), (x0, y0))
    cx = x0 + bw // 2
    slab_top = y0 + 14
    # side pillars + top beam; the arch opening between them stays sky
    draw.rectangle([cx - 32, slab_top, cx - 14, y1 - 18], fill=(38, 42, 58))
    draw.rectangle([cx + 14, slab_top, cx + 32, y1 - 18], fill=(38, 42, 58))
    draw.rectangle([cx - 32, slab_top, cx + 32, slab_top + 16],
                   fill=(38, 42, 58))
    # lit slit windows up the pillars
    for wy in range(slab_top + 22, y1 - 24, 12):
        draw.rectangle([cx - 28, wy, cx - 19, wy + 6], fill=(255, 209, 102))
        draw.rectangle([cx + 19, wy, cx + 28, wy + 6], fill=(255, 209, 102))
    # smoke plume drifting right, above the slab
    for i, (dx, dy, r) in enumerate(((0, 0, 13), (16, -8, 16),
                                     (34, -14, 12), (50, -18, 9))):
        col = (205 - i * 12, 205 - i * 12, 210 - i * 12)
        draw.ellipse([cx + dx - r, y0 + 2 + dy - r, cx + dx + r,
                      y0 + 2 + dy + r], fill=col)
    # low blocks at the tower's feet
    for bx, bh_ in ((x0 + 18, 26), (x0 + 62, 18), (x1 - 84, 22), (x1 - 40, 15)):
        draw.rectangle([bx, y1 - 18 - bh_, bx + 34, y1 - 18],
                       fill=(30, 34, 48))


def paint_court(page, draw, box):
    """The Hague: a line-art courthouse in navy on parchment, with a
    balance scale standing in front of its columns."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(233, 226, 204))
    cx = (x0 + x1) // 2
    navy = (28, 40, 66)
    # steps, columns, entablature, pediment
    for i in range(3):
        draw.rectangle([x0 + 52 + i * 10, y1 - 26 - i * 8,
                        x1 - 52 - i * 10, y1 - 18 - i * 8], fill=(196, 188, 164))
    base = y1 - 50
    for i in range(4):
        px = x0 + 66 + i * 56
        draw.rectangle([px, y0 + 62, px + 14, base], fill=(250, 247, 238),
                       outline=navy, width=2)
    draw.rectangle([x0 + 52, y0 + 50, x1 - 52, y0 + 62], fill=navy)
    draw.polygon([(x0 + 46, y0 + 50), (x1 - 46, y0 + 50), (cx, y0 + 16)],
                 fill=(250, 247, 238), outline=navy)
    # balance scale: post, beam, two pans
    draw.line([(cx, y0 + 66), (cx, y0 + 108)], fill=navy, width=4)
    draw.line([(cx - 34, y0 + 70), (cx + 34, y0 + 70)], fill=navy, width=3)
    for sx in (cx - 34, cx + 34):
        draw.line([(sx, y0 + 70), (sx, y0 + 92)], fill=navy, width=2)
        draw.pieslice([sx - 13, y0 + 88, sx + 13, y0 + 112], 0, 180,
                      fill=navy)
    draw.ellipse([cx - 4, y0 + 62, cx + 4, y0 + 70], fill=navy)


def paint_chart(page, draw, box):
    """Markets: a red area chart falling across the frame, candlesticks
    stepping down with it, and a down arrow at the end of the fall."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(250, 250, 248))
    for gy in range(y0 + 26, y1 - 10, 26):
        draw.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(228, 228, 228),
                  width=1)
    pts = [(x0 + 16, y0 + 30), (x0 + 76, y0 + 44), (x0 + 126, y0 + 40),
           (x0 + 176, y0 + 66), (x0 + 226, y0 + 62), (x0 + 276, y0 + 96),
           (x1 - 16, y0 + 112)]
    draw.polygon(pts + [(x1 - 16, y1 - 14), (x0 + 16, y1 - 14)],
                 fill=(244, 180, 180))
    draw.line(pts, fill=(178, 34, 34), width=4, joint="curve")
    for i, (cx, top, bot) in enumerate((
            (x0 + 46, 34, 52), (x0 + 106, 46, 66), (x0 + 166, 64, 84),
            (x0 + 226, 72, 94), (x0 + 282, 96, 116))):
        draw.line([(cx, y0 + top - 8), (cx, y0 + bot + 8)],
                  fill=(178, 34, 34), width=2)
        draw.rectangle([cx - 6, y0 + top, cx + 6, y0 + bot],
                       fill=(178, 34, 34))
    ax, ay = x1 - 34, y0 + 100
    draw.polygon([(ax, ay), (ax + 26, ay), (ax + 13, ay + 20)], fill=RED)


SCENES = {
    "skyline": paint_skyline,
    "tower": paint_tower,
    "court": paint_court,
    "chart": paint_chart,
}


# ---------------------------------------------------------------- content
HERO = {
    "scene": "skyline",
    "kicker": "THE DAY'S BIGGEST STORY  ·  GAMING",
    "head": "GTA VI SMASHES EVERY RECORD",
    "sub": ("Sensor Tower estimate: 24.6m copies · $2.36B on day one — "
            "and still climbing"),
}

STORIES = [
    {"scene": "tower", "kicker": "SAUDI ARABIA",
     "head": "HOUTHI STRIKE HITS RIYADH TOWER",
     "dek": ("Saudi authorities confirm the Kingdom Centre, the capital's "
            "tallest tower, was damaged in the attack.")},
    {"scene": "court", "kicker": "THE HAGUE",
     "head": "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
     "dek": ("ICJ rules 9–6 that Myanmar committed genocide against the "
            "Rohingya in northern Rakhine.")},
    {"scene": "chart", "kicker": "MARKETS",
     "head": "ASIAN MARKETS TUMBLE",
     "dek": ("Taiwan's index sheds 2,200 points intraday; Kospi and Nikkei "
            "fall as much as 4.8%.")},
]

TICKER = [
    "Cyclone Akvan hits Odisha  •  UK pledges 1,000+ drones for Ukraine (£260m)",
    "Trump pardons Pete Rose posthumously  •  Anthropic joins MSCI Large Cap + FTSE",
]

FOOTER = ("Sources: Deadline / Reuters  ·  News.Az / APA  ·  International "
          "Court of Justice  ·  market reports — all published 20 November 2026")


# ---------------------------------------------------------------- compose
def compose():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    ts = Typesetter(draw)
    f = load_fonts()

    bands = stack(0, [116, 432, 336, 84, 56])
    (my0, my1), (hy0, hy1), (cy0, cy1), (ty0, ty1), (fy0, fy1) = bands

    # masthead: the day, named up front
    draw.rectangle([0, my0, W, my1], fill=NAVY)
    draw.text((24, my0 + 18), "THE WORLD IN ONE IMAGE", font=f["kick"],
              fill=GOLD)
    side = "ONE DAY · ONE PICTURE"
    draw.text((W - 24 - f["side"].getlength(side), my0 + 18), side,
              font=f["side"], fill=(180, 190, 205))
    draw.text((24, my0 + 44), "FRIDAY 20 NOVEMBER 2026", font=f["mast"],
              fill=(255, 255, 255))
    draw.rectangle([0, my1 - 4, W, my1], fill=GOLD)

    # hero: drawn scene, headline set on a dark band across its foot
    SCENES[HERO["scene"]](page, draw, (0, hy0, W, hy1))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shade).rectangle([0, hy1 - 124, W, hy1],
                                    fill=(0, 0, 0, 170))
    page = Image.alpha_composite(page.convert("RGBA"), shade).convert("RGB")
    draw = ImageDraw.Draw(page)
    ts = Typesetter(draw)
    draw.text((24, hy1 - 112), HERO["kicker"], font=f["kick"], fill=GOLD)
    draw.text((24, hy1 - 84), HERO["head"], font=f["hero"],
              fill=(255, 255, 255))
    draw.text((24, hy1 - 30), HERO["sub"], font=f["sub"],
              fill=(225, 225, 225))

    # story cards: one drawn scene + kicker + headline + one-line dek each
    for (cx0, cx1), story in zip(cols(16, [320, 320, 320], gap=16), STORIES):
        SCENES[story["scene"]](page, draw, (cx0, cy0 + 12, cx1, cy0 + 156))
        draw.line([(cx0, cy0 + 164), (cx1, cy0 + 164)], fill=(210, 205, 190),
                  width=2)
        y = ts.para(cx0, cy0 + 176, story["kicker"], f["card_kick"], KICK,
                    cx1 - cx0)
        y = ts.para(cx0, y + 4, story["head"], f["card_head"], INK,
                    cx1 - cx0, leading=29)
        ts.para(cx0, y + 6, story["dek"], f["card_dek"], GREY, cx1 - cx0,
                leading=20)

    # ticker: what else happened today
    draw.rectangle([0, ty0, W, ty1], fill=NAVY)
    draw.rectangle([16, ty0 + 12, 168, ty1 - 12], fill=GOLD)
    ts.centred(92, ty0 + 30, "ALSO TODAY", f["tag"], NAVY)
    draw.text((184, ty0 + 10), TICKER[0], font=f["tick"],
              fill=(235, 235, 235))
    draw.text((184, ty0 + 44), TICKER[1], font=f["tick"],
              fill=(235, 235, 235))

    # footer: where it all comes from
    ts.centred(W // 2, fy0 + 18, FOOTER, f["foot"], GREY)
    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    img = compose()
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90, subsampling=0)
    data = buf.getvalue()
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)
    try:  # a copy beside this file when the repo dir is writable
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "entry.png"), "wb") as f:
            f.write(data)
    except OSError:
        pass
    print(len(data), hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
