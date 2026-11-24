"""Render the 176 x 208 dashboard through a single canvas primitive."""

from hub.bitmap import draw_bitmap
from hub.pixel_font import draw_text, text_width


WIDTH = 176
HEIGHT = 208

BACKGROUND = (6, 15, 28)
PANEL = (12, 29, 48)
SKY = (9, 23, 40)
LINE = (40, 72, 96)
MUTED = (143, 171, 194)
WHITE = (229, 246, 252)
CYAN = (117, 212, 247)
LIME = (192, 249, 82)
LIME_SHADOW = (44, 74, 43)

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
WEEKDAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")

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
    "a": (56, 108, 145), "w": (202, 234, 245),
    "b": (137, 188, 217), "c": (87, 149, 184),
}
RAIN_CLOUD_COLORS = {
    "a": (56, 108, 145), "w": (140, 181, 207),
    "b": (106, 154, 186), "c": (81, 129, 164),
}


def _draw_weather_art(canvas, condition, elapsed_ms):
    canvas.fill_rect(14, 110, 69, 66, SKY)
    for y in (116, 124, 132, 140, 148, 156, 164, 172):
        for x in (19, 27, 35, 43, 51, 59, 67, 75):
            canvas.fill_rect(x, y, 1, 1, PANEL)

    if condition == "SUNNY":
        draw_bitmap(canvas, 34, 132, SUN, SUN_COLORS, 3)
        ray = (elapsed_ms // 450) % 2
        canvas.fill_rect(49, 122 - ray, 2, 5, SUN_COLORS["y"])
        canvas.fill_rect(49, 168 + ray, 2, 4, SUN_COLORS["y"])
        canvas.fill_rect(26 - ray, 145, 5, 2, SUN_COLORS["y"])
        canvas.fill_rect(72 + ray, 145, 5, 2, SUN_COLORS["y"])
        return

    drift = (elapsed_ms // 230) % 12
    drift = min(drift, 12 - drift)
    if condition == "RAIN":
        draw_bitmap(canvas, 20 + drift, 120, CLOUD, RAIN_CLOUD_COLORS, 2)
        for index in range(6):
            y = 145 + (elapsed_ms // 65 + index * 5) % 24
            x = 23 + index * 9 - (y - 145) // 8
            canvas.fill_rect(x, y, 2, 4, CYAN)
        return

    draw_bitmap(canvas, 31, 119, SUN, SUN_COLORS, 2)
    draw_bitmap(canvas, 20 + drift, 133, CLOUD, CLOUD_COLORS, 2)
    canvas.fill_rect(66, 120, 6, 1, LINE)
    canvas.fill_rect(69, 123, 7, 1, MUTED)
    canvas.fill_rect(23, 165, 12, 1, LINE)
    canvas.fill_rect(29, 168, 12, 1, LINE)


def _center_text(canvas, center, y, value, color, scale=1):
    draw_text(canvas, center - text_width(value, scale) // 2, y,
              value, color, scale)


def render(canvas, local_time, weather, elapsed_ms):
    """Draw one complete frame. local_time uses time.localtime() tuple fields."""
    canvas.fill_rect(0, 0, WIDTH, HEIGHT, BACKGROUND)

    canvas.fill_rect(9, 11, 3, 7, LIME)
    canvas.fill_rect(14, 11, 3, 3, LIME)
    canvas.fill_rect(14, 15, 3, 3, LINE)
    draw_text(canvas, 23, 11, "N-GAGE HUB", WHITE)
    location = weather["location"]
    draw_text(canvas, 166 - text_width(location), 11, location, CYAN)
    canvas.fill_rect(8, 26, 160, 1, LINE)
    canvas.fill_rect(8, 26, 19, 1, CYAN)

    hour, minute, second = local_time[3:6]
    clock = "%02d:%02d" % (hour, minute)
    _center_text(canvas, 89, 41, clock, LIME_SHADOW, 5)
    _center_text(canvas, 88, 39, clock, LIME, 5)
    date = "%s  %02d %s" % (WEEKDAYS[local_time[6]], local_time[2],
                            MONTHS[local_time[1] - 1])
    _center_text(canvas, 88, 85, date, MUTED)
    canvas.fill_rect(12, 88, 27, 1, LINE)
    canvas.fill_rect(137, 88, 27, 1, LINE)

    canvas.fill_rect(9, 104, 158, 78, LINE)
    canvas.fill_rect(8, 105, 160, 76, LINE)
    canvas.fill_rect(9, 105, 158, 76, PANEL)
    _draw_weather_art(canvas, weather["condition"], elapsed_ms)
    canvas.fill_rect(88, 112, 1, 62, LINE)

    draw_text(canvas, 95, 115, weather["condition"], CYAN)
    draw_text(canvas, 95, 131, "%d\xb0C" % weather["temp_c"], WHITE, 3)
    draw_text(canvas, 95, 165, "H %d  L %d" % (weather["high_c"], weather["low_c"]),
              MUTED)

    canvas.fill_rect(8, 190, 160, 1, LINE)
    canvas.fill_rect(9, 197, 4, 4, LIME)
    draw_text(canvas, 17, 196, "DEMO WEATHER", MUTED)
    seconds = "SEC %02d" % second
    draw_text(canvas, 166 - text_width(seconds), 196, seconds, MUTED)
