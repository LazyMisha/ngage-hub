"""Render the 176 x 208 clock through a single canvas primitive."""

from hub.bitmap import draw_bitmap
from hub.day_cycle import draw_day_cycle
from hub.mock_weather import LODZ
from hub.pixel_font import draw_text, text_width
from hub.sunset import SUNSET_GROUND, blend, draw_sunset


WIDTH = 176
HEIGHT = 208
COLON_REGION = (84, 60, 10, 27)
CREAM = (255, 224, 170)
SHADOW = (62, 12, 5)
GOLD = (255, 166, 55)
AMBER = (238, 107, 18)

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
WEEKDAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

CARD_CORNERS = (10, 7, 5, 4, 3, 2, 2, 1, 1, 0)

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

MOON = (
    "..........hhh",
    "........hhhh",
    "......hhhhs",
    ".....hhhhss",
    "....hhhgss",
    "...hhhggss",
    "...hhgggss",
    "..hhhgggss",
    "..hhggggss",
    ".hhgggggss",
    ".hhgggggss",
    ".hhgggggss",
    ".hhgggggss",
    ".hhgggggss",
    "hhggggggss",
    ".hhggggggss",
    ".hhggggggss",
    ".hhgggggggss",
    ".hhgggggggsss",
    ".hhggggggggsss",
    "..hhggggggggsss",
    "..hhhggggggggsss",
    "...hhgggggggggssss",
    "...hhhggggggggggssssssssshhh",
    "....hhhgggggggggggsssssshhh",
    ".....hhhhggggggggggggghhhh",
    "......hhhhggggggggggghhhh",
    "........hhhhhhhghhhhhhh",
    "..........hhhhhhhhhhh",
)
MOON_COLORS = {"h": (255, 220, 126), "g": (255, 184, 51), "s": (242, 132, 21)}
SUN = (
    "....oooo.....",
    "..ooyyyyo....",
    ".oyyyyyyyo...",
    ".oywyxxxxxo..",
    "oywyyyyxxxo..",
    "oyyyyyyxxxo..",
    "oyyyyyyxxxo..",
    ".oyyyyxxxo...",
    ".oyyxxxxxo...",
    "..ooxxxoo....",
    "....ooo......",
)
SUN_COLORS = {
    "o": (193, 118, 43), "y": (255, 206, 83),
    "x": (239, 161, 57), "w": (255, 238, 154),
}
CLOUD = (
    "........aaaaaa...........",
    "......aawwwwwwaa.........",
    ".....awwwwwwwwwa.........",
    "....awwwwwwwwwwaaaa......",
    "..aawwwwwwwwwwwwwwwaa....",
    ".awwwwwwwwwwwwwwwwwwwaa..",
    ".awwwwwwwwwwwwwwwwwwwwwa.",
    "awwwwwwwwwwwwwwwwwwwwwwwa",
    "awwwwwwwwwwwwwwwwwwwwwwwa",
    "abbbbbbbbbbbbbbbbbbbbbbaa",
    ".accccccccccccccccccccaa.",
    "..aaaaaaaaaaaaaaaaaaaa...",
)
CLOUD_COLORS = {
    "a": (148, 66, 31), "w": (251, 215, 161),
    "b": (214, 154, 104), "c": (185, 119, 75),
}
RAIN_CLOUD_COLORS = {
    "a": (104, 75, 73), "w": (182, 162, 156),
    "b": (152, 127, 129), "c": (124, 100, 110),
}


def _draw_numbers(canvas, x, y, value, color, scale, show_colon):
    palette = {"#": color}
    for digit in value:
        rows = NUMBERS[digit]
        if digit != ":" or show_colon:
            draw_bitmap(canvas, x, y, rows, palette, scale)
        x += (len(rows[0]) + 1) * scale


def _draw_label(canvas, value, top, scale, ink, shadow, outlined=False):
    x = (WIDTH - text_width(value, scale)) // 2
    if outlined:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            draw_text(canvas, x + dx, top + dy, value, shadow, scale)
    else:
        draw_text(canvas, x + 1, top + 1, value, shadow, scale)
    draw_text(canvas, x, top, value, ink, scale)


def _draw_clock(canvas, local_time, top, date_top, ink, shadow, date_scale=1.5, show_colon=True):
    clock = "%02d:%02d" % (local_time[3], local_time[4])
    _draw_numbers(canvas, 28, top - 1, clock, shadow, 4, show_colon)
    _draw_numbers(canvas, 30, top + 2, clock, shadow, 4, show_colon)
    _draw_numbers(canvas, 28, top, clock, ink, 4, show_colon)
    date = "%s %02d %s" % (WEEKDAYS[local_time[6]], local_time[2],
                           MONTHS[local_time[1] - 1])
    _draw_label(canvas, date, date_top, date_scale, ink, shadow, date_scale == 2)


def _draw_card(canvas):
    height = 70
    for row in range(height):
        inset = CARD_CORNERS[min(row, height - 1 - row, 9)]
        edge = blend(GOLD, AMBER, row, height - 1)
        canvas.fill_rect(3 + inset, 112 + row, 170 - 2 * inset, 1, edge)

    for row in range(1, height - 1):
        inset = 1 + CARD_CORNERS[min(row - 1, height - 2 - row, 9)]
        left = 3 + inset
        right = 173 - inset
        y = 112 + row
        fill = blend((49, 13, 4), (65, 16, 4), row, height - 1)
        canvas.fill_rect(left, y, right - left, 1, fill)
        curve = 89 + (181 - y) ** 2 // 53
        if curve < right:
            width = min(3, right - curve)
            shade = blend((66, 18, 4), (124, 32, 3), row, height - 1)
            canvas.fill_rect(curve, y, right - curve, 1, shade)
            canvas.fill_rect(curve, y, width, 1, blend((109, 29, 3), (169, 52, 5),
                                                        row, height - 1))


def _draw_star(canvas, x, y, arm, color):
    canvas.fill_rect(x - arm, y, 2 * arm + 1, 1, color)
    canvas.fill_rect(x, y - arm, 1, 2 * arm + 1, color)


def _draw_weather_art(canvas, condition, elapsed_ms):
    pulse = (elapsed_ms // 440) % 2
    if condition == "CLEAR":
        draw_bitmap(canvas, 120, 140, MOON, MOON_COLORS, 1)
        _draw_star(canvas, 149, 141, 2 + pulse, CREAM)
        _draw_star(canvas, 157, 151, 2 - pulse, GOLD)
        return

    if condition == "SUNNY":
        draw_bitmap(canvas, 127, 141, SUN, SUN_COLORS, 2)
        canvas.fill_rect(138, 134 - pulse, 2, 5, GOLD)
        canvas.fill_rect(138, 166 + pulse, 2, 5, GOLD)
        canvas.fill_rect(119 - pulse, 150, 5, 2, GOLD)
        canvas.fill_rect(155 + pulse, 150, 5, 2, GOLD)
        return

    drift = (elapsed_ms // 230) % 10
    drift = min(drift, 10 - drift)
    if condition == "RAIN":
        draw_bitmap(canvas, 112 + drift, 137, CLOUD, RAIN_CLOUD_COLORS, 2)
        for index in range(5):
            y = 162 + (elapsed_ms // 75 + index * 4) % 12
            x = 118 + index * 8 - (y - 162) // 6
            canvas.fill_rect(x, y, 1, 3, (188, 194, 204))
        return

    draw_bitmap(canvas, 135, 136, SUN, SUN_COLORS, 2)
    draw_bitmap(canvas, 108 + drift, 151, CLOUD, CLOUD_COLORS, 2)


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


def render(canvas, local_time, weather=None, elapsed_ms=0, animate_colon=True):
    """Draw the clock with an optional weather sample."""
    if weather is None:
        ink, shadow = draw_day_cycle(canvas, WIDTH, HEIGHT, local_time[3])
        _draw_brand(canvas)
        # Seven clear pixels between rows, including shadows and city accents.
        _draw_clock(canvas, local_time, top=53, date_top=99, ink=ink,
                    shadow=shadow, date_scale=2, show_colon=False)
        _draw_label(canvas, LODZ, 128, 3, ink, shadow, True)
        if animate_colon and local_time[5] % 2 == 0:
            draw_colon(canvas, ink, shadow)
        return ink, shadow

    canvas.fill_rect(0, 0, WIDTH, HEIGHT, SUNSET_GROUND)
    draw_sunset(canvas, WIDTH, 113)
    _draw_clock(canvas, local_time, top=40, date_top=79, ink=CREAM, shadow=SHADOW)
    _draw_card(canvas)
    draw_text(canvas, 15, 119, weather["location"], CREAM, 2)
    canvas.fill_rect(13, 134, 94, 1, (170, 94, 51))
    temperature = "%d" % weather["temp_c"]
    draw_text(canvas, 16, 139, temperature, CREAM, 3)
    x = 20 + text_width(temperature, 3)
    draw_text(canvas, x, 140, "\xb0", CREAM, 2)
    draw_text(canvas, x + 9, 140, "C", CREAM, 3)
    draw_text(canvas, 16, 166, weather["condition"], CREAM, 1.5)
    _draw_weather_art(canvas, weather["condition"], elapsed_ms)
