"""Assemble entry.png: the world on Monday 23 November 2026, one page.

Layout borrowed from how the strongest broadsheet pages are built: a
date masthead with a one-line deck under it, a strip of the day's key
figures, a segmented region tally, a UTC running order, three lead
cards with scene art and in-picture tags, twelve numbered story cards
with their own scene strips, a dotted world map whose pins carry the
same numbers as the cards, a DATE CHECK panel naming older stories
left out on purpose, and a numbered also-list to close the page.
Every card carries a certainty chip (CONFIRMED, REPORTED, CLAIM or
PENDING) and the name of the outlet family it came from.

The reporting is Monday 23 November 2026's: COP31's collapse draws
calls to reform UN climate summits while its fights roll to COP32 in
Ethiopia and some ninety countries keep a voluntary 35-per-cent
electricity goal for 2035; Zelenskyy confirms naval drones sank the
Russian corvette Merkury at Benghazi and hit a second ship, and the
Kremlin warns Albania over launch claims; the European Commission
proposes sanctions on sixty banks, crypto platforms and seventy
shadow-fleet vessels; Seoul's Kospi drops 3.31 per cent on AI doubts;
Indonesia's factory-fire toll jumps to twenty-four; a magnitude 6.7
earthquake shakes Peru's Andes; Iran vows to counter the Hormuz
blockade by all means. Sources read on 24 November: Reuters, AP, AFP,
Al Jazeera, BBC, The Guardian, Just Security's Early Edition, the
Daily Summary of World and wire archives for 23 November 2026.
The picture is drawn entirely in code and is byte-stable across runs.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
MARGIN = 26
SPAN = CANVAS - 2 * MARGIN
CREAM = (247, 242, 231)
CARD_BG = (255, 253, 246)
NAVY = (17, 32, 56)
INK = (28, 28, 28)
CRIMSON = (172, 30, 46)
OCHRE = (196, 138, 30)
PINE = (34, 104, 96)
SLATE = (100, 100, 96)
SKY = (23, 40, 72)
SEA = (208, 219, 226)

TYPE = Path("/usr/share/fonts/truetype/dejavu")


def font(stem: str, size: int):
    return ImageFont.truetype(str(TYPE / stem), size)


def head_font(size: int):
    return font("DejaVuSerif-Bold.ttf", size)


def strong(size: int):
    return font("DejaVuSans-Bold.ttf", size)


def body_font(size: int):
    return font("DejaVuSans.ttf", size)


def fit_lines(text: str, fnt, limit: int) -> list[str]:
    """Greedy word wrap measured against the real font metrics."""
    scratch = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    done, pending = [], ""
    for word in text.split():
        trial = (pending + " " + word).strip()
        if scratch.textlength(trial, font=fnt) <= limit:
            pending = trial
        else:
            done.append(pending)
            pending = word
    if pending:
        done.append(pending)
    return done


# ------------------------------------------------------------ scene art
def scene_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(203, 219, 230))
    d.ellipse([x + w // 2 - 30, y + 6, x + w // 2 + 30, y + 66], fill=OCHRE)
    d.ellipse([x + w // 2 - 30, y + 6, x + w // 2 + 30, y + 66], outline=PINE, width=3)
    d.line([x + w // 2 - 30, y + 36, x + w // 2 + 30, y + 36], fill=PINE, width=2)
    d.rectangle([x + 14, y + h - 30, x + w - 14, y + h - 16], fill=(120, 82, 48))
    for i, col in enumerate([CRIMSON, PINE, OCHRE, NAVY, (96, 138, 66), (148, 88, 156)]):
        fx = x + 26 + i * (w - 52) // 5
        d.line([fx, y + h - 52, fx, y + h - 30], fill=INK, width=2)
        d.polygon([(fx, y + h - 52), (fx + 13, y + h - 46), (fx, y + h - 40)], fill=col)
    d.line([x + 6, y + 14, x + w - 6, y + h - 40], fill=CRIMSON, width=3)


def scene_fleet(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 58))
    for sx, sy in [(26, 12), (88, 7), (180, 16), (262, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(238, 238, 218))
    hull = y + h - 34
    d.polygon([(x + 60, hull), (x + 210, hull), (x + 196, hull + 16), (x + 74, hull + 16)], fill=(70, 78, 88))
    d.rectangle([x + 108, hull - 16, x + 168, hull], fill=(88, 96, 108))
    for i in range(3):
        dx, dy = x + 40 + i * 30, y + 16 + i * 8
        d.polygon([(dx, dy), (dx + 16, dy + 5), (dx, dy + 10), (dx - 6, dy + 5)], fill=(230, 230, 230))
        d.line([dx + 14, dy + 6, x + 96, hull - 10], fill=CRIMSON, width=2)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(28, 84, 110))


def scene_strait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 218, 190))
    d.polygon([(x, y + h), (x, y + 30), (x + 92, y + 52), (x + 120, y + h)], fill=(198, 168, 120))
    d.polygon([(x + w, y + h), (x + w, y + 40), (x + w - 96, y + 60), (x + w - 128, y + h)], fill=(198, 168, 120))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(28, 84, 110))
    ship_y = y + h - 30
    d.polygon([(x + w // 2 - 44, ship_y), (x + w // 2 + 44, ship_y), (x + w // 2 + 34, ship_y + 12), (x + w // 2 - 34, ship_y + 12)], fill=NAVY)
    d.rectangle([x + w // 2 - 12, ship_y - 12, x + w // 2 + 16, ship_y], fill=CRIMSON)
    d.line([x + 20, y + 16, x + w - 20, y + 16], fill=CRIMSON, width=3)


def strip_bank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 224, 214))
    for i in range(3):
        bx = x + 8 + i * (w - 16) // 3
        d.rectangle([bx, y + 10, bx + 10, y + h - 14], outline=NAVY, width=2)
    d.line([x + 4, y + h - 6, x + w - 4, y + 6], fill=CRIMSON, width=3)


def strip_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 240))
    d.line([x + 6, y + 10, x + 20, y + 20, x + 32, y + 16, x + 46, y + 34, x + w - 6, y + h - 8], fill=CRIMSON, width=3)
    d.line([x + 5, y + h - 5, x + w - 5, y + h - 5], fill=NAVY, width=2)


def strip_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 224, 208))
    d.rectangle([x + 6, y + h - 14, x + 34, y + h - 5], fill=(120, 90, 70))
    d.polygon([(x + w // 2 + 6, y + 4), (x + w // 2 + 20, y + h - 10), (x + w // 2 + 10, y + h - 3), (x + w // 2 - 4, y + h - 10)], fill=CRIMSON)
    d.polygon([(x + w // 2 + 7, y + 18), (x + w // 2 + 15, y + h - 9), (x + w // 2, y + h - 9)], fill=OCHRE)


def strip_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 216, 200))
    d.polygon([(x + 3, y + h - 6), (x + 24, y + 8), (x + 44, y + h - 6)], fill=(140, 120, 92))
    d.polygon([(x + 30, y + h - 6), (x + 50, y + 14), (x + w - 3, y + h - 6)], fill=(160, 140, 108))
    d.line([x + 8, y + h - 3, x + 24, y + h - 10, x + 38, y + h - 4, x + 54, y + h - 9], fill=CRIMSON, width=2)


def strip_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 224, 236))
    d.polygon([(x + 10, y + 12), (x + w - 10, y + 12), (x + w // 2, y + 3)], fill=NAVY)
    for i in range(4):
        bx = x + 13 + i * (w - 26) // 3
        d.rectangle([bx, y + 15, bx + 4, y + h - 10], fill=NAVY)
    d.rectangle([x + 9, y + h - 8, x + w - 9, y + h - 4], fill=NAVY)


def strip_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(208, 222, 234))
    d.polygon([(x + 6, y + h // 2 - 3), (x + w - 16, y + h // 2 - 3), (x + w - 4, y + h // 2 + 3), (x + w - 16, y + h // 2 + 6), (x + 6, y + h // 2 + 5)], fill=NAVY)
    d.polygon([(x + 14, y + h // 2 - 3), (x + 24, y + 8), (x + 30, y + 8), (x + 26, y + h // 2 - 3)], fill=CRIMSON)
    d.line([x + 4, y + h - 5, x + w - 4, y + h - 5], fill=SLATE, width=2)


def strip_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 222, 206))
    d.rectangle([x + 12, y + 6, x + 15, y + h - 5], fill=NAVY)
    d.polygon([(x + 15, y + 6), (x + 44, y + 10), (x + 15, y + 16)], fill=(52, 96, 160))
    d.polygon([(x + 34, y + 30), (x + w - 8, y + 25), (x + w - 10, y + 40), (x + 36, y + 42)], outline=CRIMSON, width=2)


def strip_dhaka(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 118, 72))
    d.ellipse([x + w // 2 - 13, y + h // 2 - 13, x + w // 2 + 13, y + h // 2 + 13], fill=CRIMSON)


def strip_train(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 210))
    d.rectangle([x + 6, y + 12, x + 42, y + h - 12], fill=NAVY)
    d.rectangle([x + 45, y + 17, x + w - 6, y + h - 12], fill=(90, 96, 106))
    for i in range(3):
        d.rectangle([x + 11 + i * 10, y + 17, x + 18 + i * 10, y + 25], fill=(240, 240, 220))
    d.line([x + 3, y + h - 4, x + w - 3, y + h - 4], fill=INK, width=2)


def strip_villa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 210, 226))
    d.rectangle([x + 14, y + 16, x + w - 14, y + h - 6], fill=(250, 248, 240))
    d.polygon([(x + 9, y + 16), (x + w - 9, y + 16), (x + w // 2, y + 5)], fill=CRIMSON)
    d.line([x + 22, y + h - 12, x + 28, y + 24], fill=(52, 120, 190), width=3)
    d.polygon([(x + w - 24, y + 8), (x + w - 17, y + 18), (x + w - 21, y + 18), (x + w - 15, y + 27)], fill=OCHRE)


def strip_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 234, 226))
    cx, cy = x + 22, y + h // 2
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=PINE)
    for dx, dy in [(-15, -10), (15, -10), (-17, 2), (17, 2), (-11, 12), (11, 12)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=PINE, width=3)
    d.rectangle([x + w - 24, y + 10, x + w - 8, y + h - 10], outline=CRIMSON, width=2)
    d.line([x + w - 16, y + 15, x + w - 16, y + h - 15], fill=CRIMSON, width=2)
    d.line([x + w - 21, y + 22, x + w - 11, y + 22], fill=CRIMSON, width=2)


def strip_rescue(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 238))
    d.polygon([(x + 8, y + 26), (x + w - 8, y + 26), (x + w - 16, y + h - 6), (x + 16, y + h - 6)], fill=NAVY)
    d.rectangle([x + 24, y + 12, x + 42, y + 26], fill=(240, 240, 240))
    d.line([x + 33, y + 15, x + 33, y + 23], fill=CRIMSON, width=3)
    d.line([x + 29, y + 19, x + 37, y + 19], fill=CRIMSON, width=3)


STRIP_ART = {"bank": strip_bank, "chart": strip_chart, "flame": strip_flame, "quake": strip_quake,
             "capitol": strip_capitol, "plane": strip_plane, "flag": strip_flag, "dhaka": strip_dhaka,
             "train": strip_train, "villa": strip_villa, "virus": strip_virus, "rescue": strip_rescue}


WORLD_DOTS = [
    "                                                                      ",
    "      #####    #        #########   ################################  ",
    "    ##########           ##############################  ##########   ",
    "     ########     ##      ###################  #################      ",
    "      ######               ################    ##############  ##     ",
    "       #####   ###          #############       ###########           ",
    "        ###     ##           ##########          ########    ###      ",
    "        ##      #             ########            ######              ",
    "         #                     ######    ##        ####     #         ",
    "                                ####    ####       ##                 ",
    "                                 ##    ######     ###                 ",
    "                                      ########   ####                 ",
    "                                       ######     ##        #         ",
    "                                        ####                    ##    ",
    "                                        ###                            ",
    "                                         #                             ",
]

PIN_SPOTS = [(0.548, 0.33, "1"), (0.515, 0.42, "2"), (0.615, 0.45, "3"), (0.80, 0.33, "5"),
             (0.755, 0.60, "7"), (0.135, 0.56, "8"), (0.475, 0.50, "13"), (0.845, 0.58, "15")]


def dotted_world(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    rows, cols = len(WORLD_DOTS), len(WORLD_DOTS[0])
    for r, row in enumerate(WORLD_DOTS):
        for c, ch in enumerate(row):
            if ch == "#":
                px = x + 8 + c * (w - 16) // cols
                py = y + 6 + r * (h - 12) // rows
                d.ellipse([px, py, px + 4, py + 4], fill=(116, 136, 152))
    for fx, fy, num in PIN_SPOTS:
        px, py = x + int(fx * w), y + int(fy * h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=CRIMSON)
        d.text((px, py), num, font=strong(11), fill=(255, 255, 255), anchor="mm")


# ------------------------------------------------------------------ data
LEADS = [
    (1, "ANTALYA · CLIMATE", "AFTER COP31: NO PACT, REFORM CALLS",
     "The summit ended Sunday without its Antalya Pact. Monday brought calls to reform UN climate summits; fights roll to COP32 in Ethiopia, and 90 countries kept a 35% electricity goal.",
     "Guardian · Reuters", "REPORTED", scene_summit, "SUMMIT FAILS"),
    (2, "BENGHAZI · SEA WAR", "UKRAINE'S DRONE WAR REACHES LIBYA",
     "Zelenskyy confirms naval drones sank the corvette Merkury at Benghazi and hit a second ship offshore. The Kremlin warns Albania after it denies the drones were launched from its territory.",
     "Reuters · Guardian", "CONFIRMED", scene_fleet, "7 NAVAL DRONES"),
    (3, "HORMUZ · STANDOFF", "IRAN VOWS TO FIGHT THE BLOCKADE",
     "Tehran says it will use every means to counter the US naval blockade of Hormuz, calling it aggression. Trump has threatened to sink Iranian tankers that try to run it.",
     "Al Jazeera · IRNA", "REPORTED", scene_strait, "BLOCKADE"),
]

CARDS = [
    (4, "bank", "BRUSSELS · SANCTIONS", "EU lines up sanctions on 60 banks", "Crypto platforms and 70 shadow-fleet vessels too; Russian teams face a flag ban.", "Commission", "REPORTED"),
    (5, "chart", "SEOUL · MARKETS", "Kospi sinks 3.31% on AI doubts", "Lowest close since January as the sell-off spreads from chips to Big Tech.", "Wires", "CONFIRMED"),
    (6, "flame", "BANTEN · DISASTER", "Factory fire toll jumps to 24", "Dozens still missing after Friday's candy-factory blaze; search goes on.", "AP · Antara", "REPORTED"),
    (7, "quake", "PERU · EARTHQUAKE", "Magnitude 6.7 quake shakes the Andes", "Tremor in the Peruvian Andes; damage checks under way in remote towns.", "USGS · Reuters", "REPORTED"),
    (8, "capitol", "WASHINGTON · POLITICS", "Democrats' 258-seat House majority", "Four races still uncalled; largest majority since 1992 stands.", "AP", "REPORTED"),
    (9, "plane", "BRUSSELS · TRAVEL", "Belgium flights grounded by strike", "Controllers walk out over austerity; most flights at Brussels grounded.", "BBC", "CONFIRMED"),
    (10, "flag", "HELSINKI · SECURITY", "Finland summons Russian ambassador", "Suspected helicopter airspace breach; Russia warns Estonia over border plan.", "Guardian", "REPORTED"),
    (11, "dhaka", "DHAKA · POLITICS", "Bangladesh: Hasina faces arrest if she returns", "State minister tells Reuters the ex-PM will be jailed on return from India.", "Reuters", "REPORTED"),
    (12, "train", "LOUISIANA · ACCIDENT", "Amtrak train derails after truck collision", "Lead locomotive and two baggage cars off the track near Lafayette.", "AP", "REPORTED"),
    (13, "villa", "ABUJA · NIGERIA", "Presidential villa hit by power and water cuts", "Tinubu says even the presidential villa suffers the outages.", "BBC", "REPORTED"),
    (14, "virus", "CONGO · HEALTH", "WHO: fighting disrupts Ebola response", "Health workers sheltered over 24 hours as clashes neared an Ituri hospital.", "WHO", "REPORTED"),
    (15, "rescue", "PHILIPPINES · AVIATION", "Air Niugini jet makes emergency landing", "146 people aboard; the plane landed safely in the Philippines.", "Wires", "REPORTED"),
]

ALSO = [
    (16, "Europe", "Abu Dhabi talks end; Medinsky restates territorial claims", "Reuters"),
    (17, "Europe", "Moldova reports seven Russian drone incursions", "Wires"),
    (18, "Europe", "NATO jets scramble over south-east Poland", "Wires"),
    (19, "Europe", "Kerch Bridge hit; Moscow says 600 drones downed", "CLAIM"),
    (20, "Europe", "Hungary's Magyar pledges Transcarpathia visit", "PENDING"),
    (21, "Europe", "French police jailed over racist assault on producer", "AFP"),
    (22, "Europe", "Romania: Georgescu moved to house arrest", "Wires"),
    (23, "Middle East", "Iran flogs singer Parastoo Ahmadi and four of her team", "Lawyers"),
    (24, "Middle East", "Oxfam: Gaza turned into a 'toxic wasteland'", "Oxfam"),
    (25, "Americas", "Trump replaces national cyber director after outages", "Wires"),
    (26, "Americas", "ICE agents make arrests at Seattle airport", "Guardian"),
    (27, "Americas", "Delta counts 2,000+ delayed flights after system failure", "AP"),
    (28, "Americas", "Court blocks pregnancy-act enforcement against Texas", "AP"),
    (29, "Asia-Pacific", "Seoul reshuffle: Kang Kum-sil to head spy agency", "Yonhap"),
    (30, "Asia-Pacific", "India offers Nepal 1.4bn-euro flood rebuild package", "Wires"),
    (31, "Asia-Pacific", "Nvidia board reinstates Jensen Huang as CEO", "Wires"),
    (32, "Asia-Pacific", "Scientists raise new cancer concerns over glyphosate", "NIH preprints"),
    (33, "Africa", "Sparta II towed back into Russian waters", "Finland"),
    (34, "Oceania", "Prespakis wins AFLW best and fairest", "ABC"),
    (35, "World", "Bitcoin rebounds to $61K after two-year low", "CoinDesk"),
]

FIGURES = [("7", "naval drones sank Merkury"), ("60", "banks in EU sanctions plan"),
           ("3.31%", "Kospi fall, lowest since Jan"), ("24", "dead in Banten fire, toll up"),
           ("6.7", "magnitude, Peru quake"), ("258", "House seats held")]


def tag_chip(d, x, y, text, colour):
    wpx = int(d.textlength(text, font=strong(10))) + 12
    d.rectangle([x, y, x + wpx, y + 16], fill=colour)
    d.text((x + 6, y + 2), text, font=strong(10), fill=(255, 255, 255))
    return wpx


def pin_badge(d, x, y, num):
    d.ellipse([x, y, x + 20, y + 20], fill=CRIMSON)
    d.text((x + 10, y + 10), str(num), font=strong(11), fill=(255, 255, 255), anchor="mm")


def render() -> Path:
    page = Image.new("RGB", (CANVAS, CANVAS), CREAM)
    d = ImageDraw.Draw(page)

    d.rectangle([0, 0, CANVAS, 26], fill=NAVY)
    d.text((MARGIN, 5), "THE WORLD IN ONE DAY", font=strong(14), fill=(255, 255, 255))
    d.text((CANVAS - MARGIN, 5), "PRESS TIME 01:30 UTC · ONE PAGE", font=strong(14),
           fill=(255, 255, 255), anchor="ra")

    d.text((CANVAS // 2, 36), "MONDAY 23 NOVEMBER 2026", font=head_font(54), fill=NAVY, anchor="ma")
    d.text((CANVAS // 2, 102), "COP31's failure brings reform calls · Ukraine's drone war reaches Libya · EU lines up new Russia sanctions",
           font=font("DejaVuSerif.ttf", 15), fill=CRIMSON, anchor="ma")
    d.text((CANVAS // 2, 124), "35 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026",
           font=strong(13), fill=NAVY, anchor="ma")
    d.line([MARGIN, 146, CANVAS - MARGIN, 146], fill=CRIMSON, width=3)

    d.rectangle([MARGIN, 154, CANVAS - MARGIN, 206], fill=NAVY)
    step = SPAN // 6
    for i, (num, label) in enumerate(FIGURES):
        cx = MARGIN + i * step + step // 2
        d.text((cx, 159), num, font=head_font(27), fill=(255, 255, 255), anchor="ma")
        d.text((cx, 190), fit_lines(label, body_font(9), step - 8)[0], font=body_font(9),
               fill=(203, 213, 228), anchor="ma")
        if i:
            d.line([MARGIN + i * step, 160, MARGIN + i * step, 200], fill=(70, 88, 116), width=1)

    d.text((MARGIN, 214), "EUROPE 11 · MIDDLE EAST 4 · AMERICAS 9 · ASIA-PACIFIC 6 · AFRICA 3 · OCEANIA 1 · WORLD 1",
           font=strong(13), fill=NAVY)
    d.text((MARGIN, 234), "THE DAY IN UTC — 10:08 Iran vows to counter blockade · 11:15 Tinubu: villa hit by cuts · 16:50 Finland summons ambassador · 17:47 EU proposes sanctions",
           font=body_font(11), fill=SLATE)

    lead_w = (SPAN - 16) // 3
    top = 254
    for i, (num, place, headline, text, source, level, scene, tag) in enumerate(LEADS):
        x = MARGIN + i * (lead_w + 8)
        d.rectangle([x, top, x + lead_w, top + 244], fill=CARD_BG, outline=NAVY, width=1)
        scene(d, x + 6, top + 6, lead_w - 12, 92)
        pin_badge(d, x + 12, top + 12, num)
        tag_chip(d, x + lead_w - 12 - (int(d.textlength(tag, font=strong(10))) + 12), top + 12, tag, CRIMSON)
        d.text((x + 10, top + 104), place, font=strong(11), fill=CRIMSON)
        lines = fit_lines(headline, head_font(17), lead_w - 20)
        for j, ln in enumerate(lines[:3]):
            d.text((x + 10, top + 119 + j * 21), ln, font=head_font(17), fill=NAVY)
        body_top = 119 + len(lines[:3]) * 21 + 4
        budget = max(1, (212 - body_top) // 13 + 1)
        body_lines = fit_lines(text, body_font(10), lead_w - 20)
        for j, ln in enumerate(body_lines[:budget]):
            d.text((x + 10, top + body_top + j * 13), ln, font=body_font(10), fill=INK)
        tag_chip(d, x + 10, top + 220, level, PINE if level != "CLAIM" else CRIMSON)
        d.text((x + 20 + int(d.textlength(level, font=strong(10))) + 12, top + 222), source,
               font=body_font(9), fill=SLATE)

    grid_y = 506
    cell_w = (SPAN - 24) // 4
    for idx, (num, art, place, headline, text, source, level) in enumerate(CARDS):
        x = MARGIN + (idx % 4) * (cell_w + 8)
        y = grid_y + (idx // 4) * 82
        d.rectangle([x, y, x + cell_w, y + 74], fill=CARD_BG, outline=(188, 182, 168), width=1)
        STRIP_ART[art](d, x + 5, y + 5, 64, 64)
        pin_badge(d, x + 8, y + 8, num)
        d.text((x + 76, y + 6), place, font=strong(9), fill=CRIMSON)
        for j, ln in enumerate(fit_lines(headline, strong(11), cell_w - 84)[:3]):
            d.text((x + 76, y + 19 + j * 13), ln, font=strong(11), fill=INK)
        d.text((x + 76, y + 60), f"{level} · {source}", font=body_font(8), fill=SLATE)

    map_y = 752
    dotted_world(d, MARGIN, map_y, 556, 100)
    d.text((MARGIN + 6, map_y + 82), "PINS MATCH STORY NUMBERS — 1 Antalya · 2 Benghazi · 3 Hormuz · 5 Seoul · 7 Banten · 8 Peru · 13 Abuja · 15 Philippines",
           font=body_font(9), fill=NAVY)
    bx = MARGIN + 568
    d.rectangle([bx, map_y, CANVAS - MARGIN, map_y + 100], fill=(252, 240, 238), outline=CRIMSON, width=2)
    d.text((bx + 10, map_y + 7), "DATE CHECK — LEFT OUT ON PURPOSE", font=strong(12), fill=CRIMSON)
    note = ("The summit itself ended on Sunday; this page covers Monday's fallout. Also left out: Korea's education "
            "minister resigns (Sun) · El Chapo Isidro captured (Sat-Sun) · Liverpool 4-0 and the ATP final (Sun) · Shenzhen summit (19-20 Nov).")
    for j, ln in enumerate(fit_lines(note, body_font(10), CANVAS - MARGIN - bx - 20)):
        d.text((bx + 10, map_y + 27 + j * 14), ln, font=body_font(10), fill=INK)

    also_y = 860
    d.rectangle([MARGIN, also_y, CANVAS - MARGIN, also_y + 23], fill=NAVY)
    d.text((MARGIN + 10, also_y + 4), "ALSO ON MONDAY 23 NOVEMBER — 20 MORE STORIES", font=strong(13),
           fill=(255, 255, 255))
    half = (len(ALSO) + 1) // 2
    for col in range(2):
        x = MARGIN + col * (SPAN // 2 + 4)
        for r, (num, region, item, source) in enumerate(ALSO[col * half:(col + 1) * half]):
            d.text((x, also_y + 29 + r * 11), f"{num}. {region}: {item} ({source})", font=body_font(10), fill=INK)

    d.line([MARGIN, 996, CANVAS - MARGIN, 996], fill=SLATE, width=1)
    d.text((MARGIN, 1000), "Sources: Reuters · AP · AFP · Al Jazeera · BBC · Guardian · Just Security · Daily Summary   |   CONFIRMED = official or 2+ outlets · REPORTED = named outlets · CLAIM = one side's account · PENDING = not settled yet",
           font=body_font(9), fill=SLATE)

    target = Path(__file__).resolve().parent / "entry.png"
    page.save(target, optimize=True)
    print("saved", target, target.stat().st_size)
    page.quantize(colors=256, method=Image.MEDIANCUT).save(target, optimize=True)
    print("quantized", target.stat().st_size, page.size)
    return target


if __name__ == "__main__":
    render()
