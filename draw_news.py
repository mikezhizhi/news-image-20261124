#!/usr/bin/env python3
"""Draw the front page summing up Tuesday 24 November 2026.

A 1024x1024 newspaper front page drawn with PIL from the stories
reported on that day. Deterministic: no clock, no network, no
randomness, no downloaded pictures. Running it twice writes the
same bytes.

Run:  python3 draw_news.py        (writes entry.png next to this file)
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
EDGE_MARGIN = 34
GAP = 16
FONTS = "/usr/share/fonts/truetype/noto/"

NEWS = (248, 244, 236)      # newsprint
PAPER_CARD = (255, 253, 248)
INK = (20, 20, 20)
GREY = (74, 72, 66)
PALE = (140, 134, 122)
LINE = (202, 195, 180)
CRIMSON = (176, 38, 30)
FOREST = (44, 108, 66)
INDIGO = (36, 64, 128)
OCHRE = (178, 122, 20)
RUST = (196, 92, 24)
PLUM = (96, 70, 150)
SLATE = (38, 62, 90)
TEAL = (22, 104, 108)

TAGS = {
    "CLIMATE": FOREST,
    "WAR": CRIMSON,
    "TECH": PLUM,
    "ASIA": SLATE,
    "POLITICS": INDIGO,
    "DISASTER": CRIMSON,
    "WORLD": RUST,
    "SPORT": TEAL,
}


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_TITLE = font("NotoSans-ExtraBold.ttf", 54)
F_DATE = font("NotoSans-Bold.ttf", 23)
F_SUB = font("NotoSans-Bold.ttf", 20)
F_LEAD_HEAD = font("NotoSans-ExtraBold.ttf", 38)
F_HEAD = font("NotoSans-Bold.ttf", 26)
F_LEAD_BODY = font("NotoSans-Regular.ttf", 22)
F_BODY = font("NotoSans-Regular.ttf", 20)
F_STRIP = font("NotoSans-Regular.ttf", 17)
F_FOOT = font("NotoSans-Regular.ttf", 16)


def fit_lines(d, text, f, width, most):
    """Greedy word wrap, capped at `most` lines."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out[:most]


def block(d, x, y, text, f, colour, width, most, step):
    """Draw wrapped text; return y below the last line."""
    for line in fit_lines(d, text, f, width, most):
        d.text((x, y), line, font=f, fill=colour)
        y += step
    return y


def chip(d, x, y, label):
    """Coloured tag chip; returns the x just past it."""
    c = TAGS[label]
    w = int(d.textlength(label, font=F_SUB)) + 18
    d.rounded_rectangle([x, y, x + w, y + 28], radius=4, fill=c)
    d.text((x + 9, y + 3), label, font=F_SUB, fill=(255, 255, 255))
    return x + w


def card(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6,
                        fill=PAPER_CARD, outline=LINE, width=2)


def star(d, cx, cy, r, colour):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)


# ---------- small scene drawings ----------

def scene_ship(d, x, y, w, h):
    """A warship listing and sinking off Libya: sea, smoke, waves."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(24, 54, 84))
    # moon
    d.ellipse([x + w - 62, y + 18, x + w - 22, y + 58], fill=(240, 232, 200))
    # smoke puffs
    for sx, sy, sr in [(x + 130, y + 52, 18), (x + 170, y + 30, 24),
                       (x + 214, y + 54, 16)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 148, 142))
    # hull, listing to starboard
    d.polygon([(x + 60, y + 150), (x + 300, y + 118), (x + 300, y + 150),
               (x + 260, y + 176), (x + 100, y + 196)],
              fill=(70, 76, 88))
    # deck and superstructure
    d.polygon([(x + 120, y + 118), (x + 210, y + 104), (x + 210, y + 130),
               (x + 120, y + 138)], fill=(96, 102, 116))
    d.rectangle([x + 236, y + 82, x + 246, y + 112], fill=(96, 102, 116))
    # fire on deck
    star(d, x + 170, y + 108, 16, (232, 96, 30))
    star(d, x + 200, y + 100, 11, (255, 214, 90))
    # waves
    for wy in (y + h - 58, y + h - 34):
        for wx in range(x + 8, x + w - 8, 52):
            d.arc([wx, wy, wx + 52, wy + 26], start=200, end=340,
                  fill=(120, 170, 210), width=4)
    d.text((x + 14, y + h - 28), "OFF LIBYA", font=F_SUB,
           fill=(255, 255, 255))


def scene_chip(d, x, y, s):
    """A green AI chip with pins, for Nvidia's CEO reversal."""
    cx, cy = x + s // 2, y + s // 2
    d.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=8,
                        fill=(24, 120, 60))
    d.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=8,
                        outline=(255, 255, 255), width=3)
    d.text((cx - 26, cy - 12), "NVDA", font=font("NotoSans-ExtraBold.ttf", 20),
           fill=(255, 255, 255))
    for i in range(4):
        px = cx - 24 + i * 16
        d.line([(px, cy - 34), (px, cy - 48)], fill=(24, 120, 60), width=4)
        d.line([(px, cy + 34), (px, cy + 48)], fill=(24, 120, 60), width=4)
        py = cy - 24 + i * 16
        d.line([(cx - 34, py), (cx - 48, py)], fill=(24, 120, 60), width=4)
        d.line([(cx + 34, py), (cx + 48, py)], fill=(24, 120, 60), width=4)


def scene_jet(d, x, y, s):
    """A fighter jet under a radar sweep, for the airspace breach."""
    # radar circle
    cx, cy = x + s // 2, y + s // 2 + 10
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=SLATE, width=3)
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=SLATE, width=2)
    d.line([(cx, cy), (cx + 34, cy - 22)], fill=CRIMSON, width=3)
    d.ellipse([cx + 30, cy - 26, cx + 38, cy - 18], fill=CRIMSON)
    # jet silhouette
    jx, jy = x + s - 44, y + 12
    d.polygon([(jx - 26, jy + 6), (jx + 6, jy), (jx - 26, jy - 6)],
              fill=INK)
    d.polygon([(jx - 18, jy + 2), (jx - 8, jy + 12), (jx - 4, jy + 2)],
              fill=INK)
    d.polygon([(jx - 18, jy - 2), (jx - 8, jy - 12), (jx - 4, jy - 2)],
              fill=INK)
    d.line([(jx - 26, jy + 6), (jx - 40, jy + 6)], fill=INK, width=2)


def scene_globe(d, x, y, s):
    """A cracked globe with a gavel mark, for COP31's failed cover text."""
    cx, cy = x + s // 2, y + s // 2 + 6
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(64, 140, 96))
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=(255, 255, 255),
              width=3)
    d.ellipse([cx - 30, cy - 28, cx - 6, cy - 4], fill=(44, 108, 66))
    d.ellipse([cx + 4, cy + 8, cx + 30, cy + 30], fill=(44, 108, 66))
    d.line([(cx - 30, cy - 38), (cx - 8, cy - 12), (cx - 20, cy + 8),
            (cx + 4, cy + 26), (cx + 28, cy + 38)],
           fill=(255, 255, 255), width=4)
    # small "no deal" cross, inside the scene box
    d.line([(cx + 30, cy - 44), (cx + 44, cy - 30)], fill=CRIMSON, width=5)
    d.line([(cx + 44, cy - 44), (cx + 30, cy - 30)], fill=CRIMSON, width=5)


def scene_capitol(d, x, y, s):
    """A capitol dome with a red RESIGNS stamp, for the Gomez ethics case."""
    cx = x + s // 2
    d.polygon([(cx - 40, y + 82), (cx + 40, y + 82), (cx + 40, y + 56),
               (cx - 40, y + 56)], fill=INDIGO)
    d.polygon([(cx - 28, y + 56), (cx + 28, y + 56), (cx, y + 32)],
              fill=INDIGO)
    d.rectangle([cx - 2, y + 26, cx + 2, y + 34], fill=INDIGO)
    for i in range(3):
        px = cx - 30 + i * 24
        d.rectangle([px, y + 62, px + 12, y + 76], fill=(255, 255, 255))
    # RESIGNS stamp
    d.rounded_rectangle([cx - 48, y + 4, cx + 48, y + 26], radius=4,
                        outline=CRIMSON, width=3)
    d.text((cx - 40, y + 7), "RESIGNS", font=font("NotoSans-ExtraBold.ttf", 14),
           fill=CRIMSON)


# ---------- page ----------

def main():
    img = Image.new("RGB", (W, H), NEWS)
    d = ImageDraw.Draw(img)
    usable = W - 2 * EDGE_MARGIN

    # Masthead
    d.line([(EDGE_MARGIN, 28), (W - EDGE_MARGIN, 28)], fill=CRIMSON, width=5)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 38), title, font=F_TITLE, fill=INK)
    dateline = "TUESDAY, 24 NOVEMBER 2026"
    dw = d.textlength(dateline, font=F_DATE)
    d.text(((W - dw) / 2, 104), dateline, font=F_DATE, fill=CRIMSON)
    strap = "THE DAY'S WORLD NEWS IN ONE IMAGE"
    sw = d.textlength(strap, font=F_SUB)
    d.text(((W - sw) / 2, 132), strap, font=F_SUB, fill=GREY)
    d.line([(EDGE_MARGIN, 160), (W - EDGE_MARGIN, 160)], fill=INK, width=3)

    # Lead: Ukraine sinks Russian warship off Libya
    ly, lh = 176, 272
    card(d, EDGE_MARGIN, ly, usable, lh)
    chip(d, EDGE_MARGIN + 18, ly + 16, "WAR")
    d.text((EDGE_MARGIN + 132, ly + 18), "MEDITERRANEAN", font=F_SUB,
           fill=PALE)
    y = block(d, EDGE_MARGIN + 18, ly + 52,
              "Ukraine sinks Russian warship off Libya",
              F_LEAD_HEAD, INK, 536, 3, 44)
    block(d, EDGE_MARGIN + 18, y + 6,
          "Kyiv's strike on a Russian naval ship in the "
          "Mediterranean shows the war reaching far beyond "
          "Europe's shores.",
          F_LEAD_BODY, GREY, 536, 5, 28)
    scene_ship(d, EDGE_MARGIN + 580, ly + 16, 356, lh - 32)

    # Middle grid: four stories
    half = (usable - GAP) // 2
    gy, gh = 464, 196
    stories = [
        ("TECH", "Nvidia rehires Huang in stunning reversal",
         "Trump pushed and JD Vance lobbied the board; "
         "Jensen Huang returns as CEO.",
         scene_chip),
        ("ASIA", "North Korean jet breaches South's airspace",
         "A suspected North Korean aircraft flies near Ulleung "
         "island; residents are ordered to shelter.",
         scene_jet),
        ("CLIMATE", "COP31 ends with no deal on cover text",
         "Negotiators fail to agree a cover text; a devastating "
         "setback for ocean-climate action.",
         scene_globe),
        ("POLITICS", "Rep. Jimmy Gomez resigns after ethics finding",
         "House Ethics finds substantial evidence of sexual "
         "misconduct with a staffer.",
         scene_capitol),
    ]
    for i, (tag_label, head, body, scene) in enumerate(stories):
        x = EDGE_MARGIN + (i % 2) * (half + GAP)
        yy = gy + (i // 2) * (gh + GAP)
        card(d, x, yy, half, gh)
        chip(d, x + 16, yy + 14, tag_label)
        y = block(d, x + 16, yy + 50, head, F_HEAD, INK, 320, 2, 31)
        block(d, x + 16, y + 4, body, F_BODY, GREY, 320, 4, 25)
        scene(d, x + half - 108, yy + 96, 92)

    # Bottom strip: disaster, world, sport
    by, bh = 888, 84
    card(d, EDGE_MARGIN, by, usable, bh)
    third = usable // 3
    strip = [
        ("DISASTER", "Fire engulfs six hotels on Zanzibar; 180 tourists evacuated"),
        ("WORLD", "Hacked data puts Russian war dead near 500,000"),
        ("SPORT", "US, Mexico, Costa Rica and Jamaica to host 2031 Women's World Cup"),
    ]
    for i, (label, text) in enumerate(strip):
        x = EDGE_MARGIN + 16 + i * third
        d.text((x, by + 12), label, font=F_SUB, fill=TAGS[label])
        block(d, x, by + 38, text, F_STRIP, INK, third - 32, 2, 21)
        if i:
            d.line([(EDGE_MARGIN + i * third, by + 12),
                    (EDGE_MARGIN + i * third, by + bh - 12)],
                   fill=LINE, width=2)

    # Footer
    foot = ("All events reported on Tuesday 24 November 2026  ·  "
            "make.fun news-image-20261124")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 986), foot, font=F_FOOT, fill=PALE)

    img.save("entry.png", optimize=True)
    print(f"wrote entry.png ({W}x{H})")


if __name__ == "__main__":
    main()
