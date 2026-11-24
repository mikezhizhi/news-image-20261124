#!/usr/bin/env python3
"""Tuesday 24 November 2026, drawn as a one-page newspaper.

PIL draws the whole front page: masthead, lead story, four middle
stories and a three-item strip at the bottom. No network, no clock,
no randomness and no downloaded pictures, so running the script
twice writes identical bytes.

Usage: python3 draw_news.py   # writes entry.png beside this file
"""

import math

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 34
GAP = 16
FONT_DIR = "/usr/share/fonts/truetype/noto/"

PAPER = (248, 244, 236)
CARD_BG = (255, 253, 248)
TEXT = (20, 20, 20)
SECONDARY = (74, 72, 66)
FAINT = (140, 134, 122)
RULE = (202, 195, 180)
RED = (176, 38, 30)
GREEN = (44, 108, 66)
BLUE = (36, 64, 128)
AMBER = (178, 122, 20)
ORANGE = (196, 92, 24)
PURPLE = (96, 70, 150)
NAVY = (38, 62, 90)
TEAL = (22, 104, 108)

SECTION_COLOURS = {
    "WAR": RED,
    "TECH": PURPLE,
    "ASIA": NAVY,
    "CLIMATE": GREEN,
    "POLITICS": BLUE,
    "DISASTER": RED,
    "WORLD": ORANGE,
    "SPORT": TEAL,
}


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


TITLE_FONT = load("NotoSans-ExtraBold.ttf", 54)
DATE_FONT = load("NotoSans-Bold.ttf", 23)
LABEL_FONT = load("NotoSans-Bold.ttf", 20)
LEAD_HEAD_FONT = load("NotoSans-ExtraBold.ttf", 38)
HEAD_FONT = load("NotoSans-Bold.ttf", 26)
LEAD_BODY_FONT = load("NotoSans-Regular.ttf", 22)
BODY_FONT = load("NotoSans-Regular.ttf", 20)
STRIP_FONT = load("NotoSans-Regular.ttf", 17)
FOOT_FONT = load("NotoSans-Regular.ttf", 16)


def wrap(draw, text, face, width, limit):
    """Greedy word wrap, at most `limit` lines."""
    lines, current = [], ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:limit]


def para(draw, x, y, text, face, colour, width, limit, leading):
    """Draw wrapped text and return the y below its last line."""
    for line in wrap(draw, text, face, width, limit):
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def tag(draw, x, y, label):
    """Draw a coloured section tag; return the x just past it."""
    colour = SECTION_COLOURS[label]
    width = int(draw.textlength(label, font=LABEL_FONT)) + 18
    draw.rounded_rectangle([x, y, x + width, y + 28], radius=4, fill=colour)
    draw.text((x + 9, y + 3), label, font=LABEL_FONT, fill=(255, 255, 255))
    return x + width


def box(draw, x, y, width, height):
    draw.rounded_rectangle([x, y, x + width, y + height], radius=6,
                           fill=CARD_BG, outline=RULE, width=2)


def burst(draw, cx, cy, radius, colour):
    points = []
    for i in range(16):
        angle = math.pi * i / 8
        r = radius if i % 2 == 0 else radius * 0.45
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=colour)


# ---------- little pictures for each story ----------

def draw_ship_scene(draw, x, y, width, height):
    """A listing warship on a night sea, smoke above it, off Libya."""
    draw.rounded_rectangle([x, y, x + width, y + height], radius=6,
                           fill=(24, 54, 84))
    # pale moon
    draw.ellipse([x + width - 62, y + 18, x + width - 22, y + 58],
                 fill=(240, 232, 200))
    # smoke rising from the deck
    for sx, sy, sr in ((x + 130, y + 52, 18), (x + 170, y + 30, 24),
                       (x + 214, y + 54, 16)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(150, 148, 142))
    # hull, listing to starboard
    draw.polygon([(x + 60, y + 150), (x + 300, y + 118), (x + 300, y + 150),
                  (x + 260, y + 176), (x + 100, y + 196)],
                 fill=(70, 76, 88))
    # deckhouse and mast
    draw.polygon([(x + 120, y + 118), (x + 210, y + 104), (x + 210, y + 130),
                  (x + 120, y + 138)], fill=(96, 102, 116))
    draw.rectangle([x + 236, y + 82, x + 246, y + 112], fill=(96, 102, 116))
    # fire on the deck
    burst(draw, x + 170, y + 108, 16, (232, 96, 30))
    burst(draw, x + 200, y + 100, 11, (255, 214, 90))
    # waves along the bottom
    for wy in (y + height - 58, y + height - 34):
        for wx in range(x + 8, x + width - 8, 52):
            draw.arc([wx, wy, wx + 52, wy + 26], start=200, end=340,
                     fill=(120, 170, 210), width=4)
    draw.text((x + 14, y + height - 28), "OFF LIBYA", font=LABEL_FONT,
              fill=(255, 255, 255))


def draw_chip_scene(draw, x, y, size):
    """A green AI chip stamped NVDA, for the Nvidia CEO reversal."""
    cx, cy = x + size // 2, y + size // 2
    draw.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=8,
                           fill=(24, 120, 60))
    draw.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=8,
                           outline=(255, 255, 255), width=3)
    draw.text((cx - 26, cy - 12), "NVDA",
              font=load("NotoSans-ExtraBold.ttf", 20), fill=(255, 255, 255))
    for i in range(4):
        px = cx - 24 + i * 16
        draw.line([(px, cy - 34), (px, cy - 48)], fill=(24, 120, 60), width=4)
        draw.line([(px, cy + 34), (px, cy + 48)], fill=(24, 120, 60), width=4)
        py = cy - 24 + i * 16
        draw.line([(cx - 34, py), (cx - 48, py)], fill=(24, 120, 60), width=4)
        draw.line([(cx + 34, py), (cx + 48, py)], fill=(24, 120, 60), width=4)


def draw_jet_scene(draw, x, y, size):
    """A jet under a radar sweep, for the airspace breach."""
    cx, cy = x + size // 2, y + size // 2 + 10
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=NAVY, width=3)
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=NAVY, width=2)
    draw.line([(cx, cy), (cx + 34, cy - 22)], fill=RED, width=3)
    draw.ellipse([cx + 30, cy - 26, cx + 38, cy - 18], fill=RED)
    # jet silhouette, nose to the right
    jx, jy = x + size - 44, y + 12
    draw.polygon([(jx - 26, jy + 6), (jx + 6, jy), (jx - 26, jy - 6)],
                 fill=TEXT)
    draw.polygon([(jx - 18, jy + 2), (jx - 8, jy + 12), (jx - 4, jy + 2)],
                 fill=TEXT)
    draw.polygon([(jx - 18, jy - 2), (jx - 8, jy - 12), (jx - 4, jy - 2)],
                 fill=TEXT)
    draw.line([(jx - 26, jy + 6), (jx - 40, jy + 6)], fill=TEXT, width=2)


def draw_globe_scene(draw, x, y, size):
    """A cracked globe with a red cross, for COP31's failed cover text."""
    cx, cy = x + size // 2, y + size // 2 + 6
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(64, 140, 96))
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40],
                 outline=(255, 255, 255), width=3)
    draw.ellipse([cx - 30, cy - 28, cx - 6, cy - 4], fill=(44, 108, 66))
    draw.ellipse([cx + 4, cy + 8, cx + 30, cy + 30], fill=(44, 108, 66))
    # crack across the globe
    draw.line([(cx - 30, cy - 38), (cx - 8, cy - 12), (cx - 20, cy + 8),
               (cx + 4, cy + 26), (cx + 28, cy + 38)],
              fill=(255, 255, 255), width=4)
    # small "no deal" cross, kept inside the scene
    draw.line([(cx + 30, cy - 44), (cx + 44, cy - 30)], fill=RED, width=5)
    draw.line([(cx + 44, cy - 44), (cx + 30, cy - 30)], fill=RED, width=5)


def draw_dome_scene(draw, x, y, size):
    """A capitol dome under a red RESIGNS stamp, for the ethics case."""
    cx = x + size // 2
    draw.polygon([(cx - 40, y + 82), (cx + 40, y + 82), (cx + 40, y + 56),
                  (cx - 40, y + 56)], fill=BLUE)
    draw.polygon([(cx - 28, y + 56), (cx + 28, y + 56), (cx, y + 32)],
                 fill=BLUE)
    draw.rectangle([cx - 2, y + 26, cx + 2, y + 34], fill=BLUE)
    for i in range(3):
        px = cx - 30 + i * 24
        draw.rectangle([px, y + 62, px + 12, y + 76], fill=(255, 255, 255))
    # RESIGNS stamp above the dome
    draw.rounded_rectangle([cx - 48, y + 4, cx + 48, y + 26], radius=4,
                           outline=RED, width=3)
    draw.text((cx - 40, y + 7), "RESIGNS",
              font=load("NotoSans-ExtraBold.ttf", 14), fill=RED)


# ---------- the page itself ----------

def build_page():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    content = PAGE - 2 * MARGIN

    # Masthead
    draw.line([(MARGIN, 28), (PAGE - MARGIN, 28)], fill=RED, width=5)
    masthead = "THE WORLD IN ONE DAY"
    mw = draw.textlength(masthead, font=TITLE_FONT)
    draw.text(((PAGE - mw) / 2, 38), masthead, font=TITLE_FONT, fill=TEXT)
    dateline = "TUESDAY, 24 NOVEMBER 2026"
    dw = draw.textlength(dateline, font=DATE_FONT)
    draw.text(((PAGE - dw) / 2, 104), dateline, font=DATE_FONT, fill=RED)
    strap = "THE DAY'S WORLD NEWS IN ONE IMAGE"
    sw = draw.textlength(strap, font=LABEL_FONT)
    draw.text(((PAGE - sw) / 2, 132), strap, font=LABEL_FONT, fill=SECONDARY)
    draw.line([(MARGIN, 160), (PAGE - MARGIN, 160)], fill=TEXT, width=3)

    # Lead story: Ukraine sinks a Russian warship off Libya
    lead_y, lead_h = 176, 272
    box(draw, MARGIN, lead_y, content, lead_h)
    tag(draw, MARGIN + 18, lead_y + 16, "WAR")
    draw.text((MARGIN + 132, lead_y + 18), "MEDITERRANEAN",
              font=LABEL_FONT, fill=FAINT)
    y = para(draw, MARGIN + 18, lead_y + 52,
             "Ukraine sinks Russian warship off Libya",
             LEAD_HEAD_FONT, TEXT, 536, 3, 44)
    para(draw, MARGIN + 18, y + 6,
         "Kyiv's strike on a Russian naval ship in the "
         "Mediterranean shows the war reaching far beyond "
         "Europe's shores.",
         LEAD_BODY_FONT, SECONDARY, 536, 5, 28)
    draw_ship_scene(draw, MARGIN + 580, lead_y + 16, 356, lead_h - 32)

    # Four stories in a two-by-two grid
    half = (content - GAP) // 2
    grid_y, grid_h = 464, 196
    middle = [
        ("TECH", "Nvidia rehires Huang in stunning reversal",
         "Trump pushed and JD Vance lobbied the board; "
         "Jensen Huang returns as CEO.",
         draw_chip_scene),
        ("ASIA", "North Korean jet breaches South's airspace",
         "A suspected North Korean aircraft flies near Ulleung "
         "island; residents are ordered to shelter.",
         draw_jet_scene),
        ("CLIMATE", "COP31 ends with no deal on cover text",
         "Negotiators fail to agree a cover text; a devastating "
         "setback for ocean-climate action.",
         draw_globe_scene),
        ("POLITICS", "Rep. Jimmy Gomez resigns after ethics finding",
         "House Ethics finds substantial evidence of sexual "
         "misconduct with a staffer.",
         draw_dome_scene),
    ]
    for i, (section, headline, body, picture) in enumerate(middle):
        x = MARGIN + (i % 2) * (half + GAP)
        yy = grid_y + (i // 2) * (grid_h + GAP)
        box(draw, x, yy, half, grid_h)
        tag(draw, x + 16, yy + 14, section)
        y = para(draw, x + 16, yy + 50, headline, HEAD_FONT, TEXT, 320, 2, 31)
        para(draw, x + 16, y + 4, body, BODY_FONT, SECONDARY, 320, 4, 25)
        picture(draw, x + half - 108, yy + 96, 92)

    # Bottom strip: disaster, world, sport
    strip_y, strip_h = 888, 84
    box(draw, MARGIN, strip_y, content, strip_h)
    third = content // 3
    strip = [
        ("DISASTER", "Fire engulfs six hotels on Zanzibar; 180 tourists evacuated"),
        ("WORLD", "Hacked data puts Russian war dead near 500,000"),
        ("SPORT", "US, Mexico, Costa Rica and Jamaica to host 2031 Women's World Cup"),
    ]
    for i, (section, text) in enumerate(strip):
        x = MARGIN + 16 + i * third
        draw.text((x, strip_y + 12), section, font=LABEL_FONT,
                  fill=SECTION_COLOURS[section])
        para(draw, x, strip_y + 38, text, STRIP_FONT, TEXT, third - 32, 2, 21)
        if i:
            draw.line([(MARGIN + i * third, strip_y + 12),
                       (MARGIN + i * third, strip_y + strip_h - 12)],
                      fill=RULE, width=2)

    # Footer
    footer = ("All events reported on Tuesday 24 November 2026  ·  "
              "make.fun news-image-20261124")
    fw = draw.textlength(footer, font=FOOT_FONT)
    draw.text(((PAGE - fw) / 2, 986), footer, font=FOOT_FONT, fill=FAINT)
    return img


def main():
    page = build_page()
    page.save("entry.png", optimize=True)
    print("wrote entry.png ({}x{})".format(PAGE, PAGE))


if __name__ == "__main__":
    main()
