#!/usr/bin/env python3
"""news-image-20261120: compose a newspaper front page summing up
Friday 20 November 2026 in one 1024x1024 image.

Deterministic: stdlib + PIL only, no network, no randomness, no timestamps.
Reads the four text-free panels in assets/ and renders every word with PIL
fonts, so nothing on the page can be garbled. Writes entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png and to this directory.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
RULE = (26, 26, 26)
ACCENT = (163, 22, 33)
SUB = (74, 74, 74)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(im, tw, th):
    """Center-crop image to exactly tw x th (keeps aspect by cropping)."""
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return im.crop((x, y, x + tw, y + th))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def center_text(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def compose():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead ----
    center_text(d, 22, "THE DAY IN ONE PICTURE", font(SANS_BOLD, 21), ACCENT)
    center_text(d, 50, "FRIDAY 20 NOVEMBER 2026", font(SERIF, 46), INK)
    d.line([(28, 108), (996, 108)], fill=RULE, width=3)
    d.line([(28, 114), (996, 114)], fill=RULE, width=1)

    # ---- Dominant panel: GTA VI ----
    gta = Image.open(ASSETS / "panel-gta.webp").convert("RGB")
    page.paste(cover_crop(gta, 968, 392), (28, 126))
    d.rectangle([28, 126, 996, 518], outline=RULE, width=2)
    center_text(d, 528, "GTA VI SMASHES EVERY RECORD", font(SERIF, 40), INK)
    center_text(
        d,
        574,
        "Sensor Tower est.: 24.6m copies \u00b7 $2.36B on day one \u2014 and still climbing",
        font(SANS, 23),
        SUB,
    )
    d.line([(28, 612), (996, 612)], fill=RULE, width=2)

    # ---- Three small panels ----
    panels = [
        (
            "panel-riyadh.webp",
            "HOUTHI STRIKE HITS RIYADH TOWER",
            "Saudi confirms attack damaged its tallest skyscraper",
        ),
        (
            "panel-icj.webp",
            "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
            "ICJ rules for the Rohingya, 9\u20136, in landmark case",
        ),
        (
            "panel-markets.webp",
            "ASIAN MARKETS TUMBLE",
            "Taiwan sheds 2,200 pts; Kospi, Nikkei down ~5%",
        ),
    ]
    x0s = (28, 356, 684)
    for (fname, head, sub), x0 in zip(panels, x0s):
        im = Image.open(ASSETS / fname).convert("RGB")
        page.paste(cover_crop(im, 312, 196), (x0, 626))
        d.rectangle([x0, 626, x0 + 312, 822], outline=RULE, width=2)
        lines = wrap(d, head, font(SANS_BOLD, 21), 312)
        y = 834
        for line in lines:
            d.text((x0, y), line, font=font(SANS_BOLD, 21), fill=INK)
            y += 26
        sub_lines = wrap(d, sub, font(SANS, 16), 312)
        y += 4
        for line in sub_lines:
            d.text((x0, y), line, font=font(SANS, 16), fill=SUB)
            y += 20

    # ---- Ticker ----
    d.line([(28, 936), (996, 936)], fill=RULE, width=2)
    ticker = (
        "ALSO: Cyclone Akvan makes landfall in Odisha \u00b7 UK pledges 1,000 drones "
        "for Ukraine \u00b7 Trump pardons baseball's Pete Rose \u00b7 Anthropic joins "
        "MSCI + FTSE after record IPO"
    )
    lines = wrap(d, ticker, font(SANS, 17), 968)
    y = 948
    for line in lines:
        d.text((28, y), line, font=font(SANS, 17), fill=SUB)
        y += 22

    return page


def main():
    page = compose()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    targets = [BASE / "entry.png"]
    if out_dir:
        targets.append(Path(out_dir) / "entry.png")
    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        page.save(target, "JPEG", quality=88, optimize=True)
        print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
