"""Render the 176 x 208 clock through a single canvas primitive."""

from hub.bitmap import draw_bitmap
from hub.day_cycle import draw_day_cycle
from hub.pixel_font import draw_text, text_width


WIDTH = 176
HEIGHT = 208
COLON_REGION = (84, 60, 10, 27)
LODZ = u"\u0141\u00d3D\u0179"

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
WEEKDAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

NUMBERS = {
    "0": ".####. ###### ##..## ##..## ##..## ##..## ##..## ###### .####.",
    "1": "..##.. .###.. ####.. ..##.. ..##.. ..##.. ..##.. ..##.. ######",
    "2": ".####. ###### ##..## ....## ...##. ..##.. .##... ##.... ######",
    "3": ".####. ###### ....## ....## ..###. ....## ....## ###### .####.",
    "4": "....## ...### ..#.## .#..## ##..## ###### ###### ....## ....##",
    "5": "###### ##.... ##.... #####. .##### ....## ....## ###### .####.",
    "6": "..###. .##... ##.... #####. ###### ##..## ##..## ###### .####.",
    "7": "###### ....## ...##. ...##. ..##.. ..##.. .##... .##... .##...",
    "8": ".####. ###### ##..## ##..## .####. ##..## ##..## ###### .####.",
    "9": ".####. ###### ##..## ##..## ###### .##### ....## ...##. .###..",
    ":": ".. .. ## ## .. .. ## ## ..",
}
for digit in NUMBERS:
    NUMBERS[digit] = NUMBERS[digit].split()

def _draw_numbers(canvas, x, y, value, color, scale):
    palette = {"#": color}
    for digit in value:
        rows = NUMBERS[digit]
        if digit != ":":
            draw_bitmap(canvas, x, y, rows, palette, scale)
        x += (len(rows[0]) + 1) * scale


def _draw_label(canvas, value, top, scale, ink, shadow):
    x = (WIDTH - text_width(value, scale)) // 2
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw_text(canvas, x + dx, top + dy, value, shadow, scale)
    draw_text(canvas, x, top, value, ink, scale)


def _draw_clock(canvas, local_time, top, date_top, ink, shadow):
    clock = "%02d:%02d" % (local_time[3], local_time[4])
    _draw_numbers(canvas, 28, top - 1, clock, shadow, 4)
    _draw_numbers(canvas, 30, top + 2, clock, shadow, 4)
    _draw_numbers(canvas, 28, top, clock, ink, 4)
    date = "%s %02d %s" % (WEEKDAYS[local_time[6]], local_time[2],
                           MONTHS[local_time[1] - 1])
    _draw_label(canvas, date, date_top, 2, ink, shadow)


BRAND_GLYPHS = (
    ("##....## ###...## ####..## ##.##.## ##..#### ##...### ##....##", (255, 58, 48)),
    ("........ ........ ........ .######. ........ ........ ........", (255, 58, 48)),
    ("..###### .##..... .##..... .##..### .##...## .##...## ..######", (235, 242, 248)),
    ("...####. .##..##. .##..##. .######. .##..##. .##..##. .##..##.", (235, 242, 248)),
    ("...##### .##..... .##..... .##..### .##...## .##...## ..######", (235, 242, 248)),
    ("..###### .##..... .##..... .######. .##..... .##..... ..######", (235, 242, 248)),
)


def _draw_brand(canvas):
    x = (WIDTH - (len(BRAND_GLYPHS) * 9 - 1) * 2) // 2
    for glyph, color in BRAND_GLYPHS:
        rows = glyph.split()
        draw_bitmap(canvas, x + 1, 25, rows, {"#": (18, 23, 32)}, 2)
        draw_bitmap(canvas, x, 23, rows, {"#": color}, 2)
        x += 18


def draw_colon(canvas, ink, shadow):
    dots = NUMBERS[":"]
    draw_bitmap(canvas, 84, 52, dots, {"#": shadow}, 4)
    draw_bitmap(canvas, 86, 55, dots, {"#": shadow}, 4)
    draw_bitmap(canvas, 84, 53, dots, {"#": ink}, 4)


def render(canvas, local_time, animate_colon=True):
    """Draw the clock and skyline for the device's current local time."""
    ink, shadow = draw_day_cycle(canvas, WIDTH, HEIGHT, local_time[3])
    _draw_brand(canvas)
    # Seven clear pixels between rows, including shadows and city accents.
    _draw_clock(canvas, local_time, top=53, date_top=99, ink=ink,
                shadow=shadow)
    _draw_label(canvas, LODZ, 128, 3, ink, shadow)
    if animate_colon and local_time[5] % 2 == 0:
        draw_colon(canvas, ink, shadow)
    return ink, shadow
