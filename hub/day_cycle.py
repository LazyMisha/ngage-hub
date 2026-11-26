"""Half-hour sky scenes selected by the clock's local time."""

from hub.bitmap import draw_bitmap
from hub.sunset import SKYLINE_BASE, SUNSET_GROUND, blend, draw_sky, draw_skyline, draw_sunset


HORIZON_Y = 186
INK = (255, 224, 170)
SHADOW = (62, 12, 5)

# Ordered in two-hour slots from midnight.
# Name, three sky colors, celestial body (kind, x, y), star count, light lettering.
SCENES = (
    ("Midnight", ((8, 12, 30), (18, 26, 59), (40, 56, 96)),
     ("moon", 139, 25), 22, True),
    ("Deep night", ((18, 12, 35), (42, 29, 70), (85, 55, 105)),
     ("moon", 108, 22), 16, True),
    ("Before dawn", ((23, 19, 50), (56, 40, 84), (206, 111, 139)),
     ("moon", 43, 26), 8, True),
    ("Sunrise", ((84, 63, 124), (208, 135, 156), (255, 187, 112)),
     ("sun", 58, 171), 0, False),
    ("Early morning", ((80, 136, 192), (153, 200, 232), (255, 221, 176)),
     ("sun", 35, 125), 0, False),
    ("Late morning", ((46, 123, 158), (116, 199, 209), (209, 244, 219)),
     ("sun", 49, 33), 0, False),
    ("High noon", ((53, 106, 187), (125, 190, 241), (206, 236, 248)),
     ("sun", 91, 24), 0, False),
    ("Afternoon", ((89, 121, 171), (173, 198, 227), (251, 218, 164)),
     ("sun", 135, 38), 0, False),
    ("Golden hour", ((142, 75, 97), (228, 146, 101), (255, 203, 105)),
     ("sun", 146, 139), 0, False),
    ("Sunset", None, None, 0, True),
    ("Dusk", ((38, 28, 64), (78, 50, 103), (196, 98, 113)),
     ("moon", 130, 25), 7, True),
    ("Late evening", ((14, 23, 46), (30, 56, 101), (71, 105, 151)),
     ("moon", 151, 34), 15, True),
)

STARS = (
    (13, 15), (162, 17), (82, 31), (153, 77), (16, 53), (121, 13), (11, 118),
    (51, 15), (121, 35), (38, 38), (66, 8), (167, 48), (48, 105), (158, 135),
    (26, 31), (100, 16), (18, 91), (143, 117), (75, 44), (108, 42), (11, 147),
    (158, 103),
)

MOON = (
    ".....hhh",
    "...hhh",
    "..hhg",
    ".hhgg",
    ".hggg",
    "hhggg",
    "hhgggg",
    "hhggggg",
    ".hggggggg",
    ".hhggggggggh",
    "..hhggggggh",
    "....hhhhhh",
)
SUN_WIDTHS = (3, 7, 9, 11, 13, 13, 15, 15, 15, 13, 13, 11, 9, 7, 3)

CLOUD_BANDS = (
    (3, 43, 32), (120, 52, 46), (4, 115, 28),
    (118, 109, 45), (4, 135, 55), (109, 145, 58), (42, 156, 54),
)


def _draw_clouds(canvas, top, middle, horizon, slot, light_lettering):
    shift = slot % 3 * 4
    for x, y, span in CLOUD_BANDS:
        if y < 95:
            color = blend(top, middle, y, 95)
        else:
            color = blend(middle, horizon, y - 95, HORIZON_Y - 95)
        if light_lettering:
            color = blend(color, horizon, 1, 5)
        else:
            color = blend(color, (255, 237, 222), 2, 5)
        canvas.fill_rect(x + shift + span // 5, y, span * 3 // 5, 1, color)
        canvas.fill_rect(x + shift, y + 1, span, 1, color)
        canvas.fill_rect(x + shift + span // 8, y + 2, span * 3 // 4, 1, color)


def _draw_stars(canvas, count, top, horizon):
    faint = blend(top, (210, 218, 246), 1, 2)
    bright = blend(horizon, (244, 223, 219), 2, 3)
    for index in range(count):
        x, y = STARS[index]
        if index % 5 == 0:
            canvas.fill_rect(x - 1, y, 3, 1, bright)
            canvas.fill_rect(x, y - 1, 1, 3, bright)
        else:
            canvas.fill_rect(x, y, 1, 1, faint)


def _draw_celestial_body(canvas, body, horizon):
    kind, x, y = body
    if kind == "moon":
        palette = {"h": (246, 234, 211), "g": blend(horizon, (232, 215, 205), 3, 4)}
        draw_bitmap(canvas, x - 6, y - 6, MOON, palette, 1)
        return

    glow = blend(horizon, (255, 233, 159), 1, 2)
    for row in range(len(SUN_WIDTHS)):
        span = SUN_WIDTHS[row]
        canvas.fill_rect(x - span // 2 - 2, y - 8 + row, span + 4, 3, glow)
    for row in range(len(SUN_WIDTHS)):
        span = SUN_WIDTHS[row]
        color = (255, 245, 203)
        if row >= 9:
            color = (255, 221, 143)
        canvas.fill_rect(x - span // 2, y - 7 + row, span, 1, color)


def _draw_anchor_scene(canvas, width, height, slot):
    _, colors, body, stars, light_lettering = SCENES[slot]
    if colors is None:
        canvas.fill_rect(0, 0, width, height, SUNSET_GROUND)
        draw_sunset(canvas, width, HORIZON_Y)
        return INK, SHADOW

    top, middle, horizon = colors
    ground = blend((6, 11, 23), middle, 1, 5)
    distant = blend(ground, horizon, 1, 5)
    brick = blend(ground, distant, 1, 3)
    canvas.fill_rect(0, 0, width, height, ground)
    draw_sky(canvas, width, HORIZON_Y, ((0, top), (55, middle), (SKYLINE_BASE, horizon)))
    _draw_clouds(canvas, top, middle, horizon, slot, light_lettering)
    _draw_stars(canvas, stars, top, horizon)
    _draw_celestial_body(canvas, body, horizon)
    if light_lettering:
        windows = blend(horizon, (248, 177, 100), 2, 3)
        lettering = (INK, (20, 17, 34))
    else:
        windows = blend(distant, horizon, 1, 4)
        lettering = ((18, 30, 49), blend(middle, (255, 239, 219), 2, 3))
    draw_skyline(canvas, HORIZON_Y, distant, brick, windows)
    return lettering


PALETTES = [scene[1] for scene in SCENES]
PALETTES[9] = ((54, 13, 17), (187, 45, 20), (248, 104, 11))
BODIES = [scene[2] for scene in SCENES]
BODIES[9] = ("sun", 139, 175)
# Hand-position the sun near the horizon and bring the moon in from the edge.
TRANSITIONS = {
    2: (("moon", 33, 33), ("moon", 21, 40), ("sun", 49, 184)),
    9: (("sun", 145, 181), ("sun", 151, 187), ("moon", 123, 33)),
}
# Small color accents distinguish the half-hour scenes while keeping the day coherent.
ACCENTS = [
    (53, 84, 143), (102, 60, 134), (239, 135, 148),
    (255, 189, 121), (115, 206, 216), (116, 194, 246),
    (104, 170, 236), (247, 197, 159), (255, 126, 62),
    (194, 59, 97), (119, 109, 173), (68, 96, 145),
]


def draw_day_cycle(canvas, width, height, hour, minute=0):
    """Paint the half-hour scene and return its clock ink and shadow."""
    slot = hour * 2 + minute // 30
    anchor, step = divmod(slot, 4)
    if step == 0:
        return _draw_anchor_scene(canvas, width, height, anchor)
    following = (anchor + 1) % 12
    top, middle, horizon = [
        blend(a, b, step, 4) for a, b in zip(PALETTES[anchor], PALETTES[following])
    ]
    middle = blend(middle, ACCENTS[anchor], (2, 3, 2)[step - 1], 14)
    horizon = blend(horizon, ACCENTS[anchor], (2, 3, 2)[step - 1], 13)
    light = (middle[0] * 3 + middle[1] * 6 + middle[2]) < 1050
    ground = blend((6, 11, 23), middle, 1, 5)
    distant = blend(ground, horizon, 1, 5)
    brick = blend(ground, distant, 1, 3)
    canvas.fill_rect(0, 0, width, height, ground)
    draw_sky(canvas, width, HORIZON_Y, ((0, top), (55, middle), (SKYLINE_BASE, horizon)))
    _draw_clouds(canvas, top, middle, horizon, slot, light)
    if anchor in (2, 8, 9, 10):
        for x, y, span in ((2, 158, 42), (99, 166, 60), (42, 174, 54)):
            color = blend(middle, horizon, 3, 4)
            color = blend(color, ACCENTS[anchor], 2, 7)
            canvas.fill_rect(x + step * 3, y - step, span, 1, color)
            canvas.fill_rect(x + step * 3 + 5, y + 1 - step, span - 12, 1, color)
    stars_a, stars_b = SCENES[anchor][3], SCENES[following][3]
    _draw_stars(canvas, stars_a + (stars_b - stars_a) * step // 4, top, horizon)
    if anchor in TRANSITIONS:
        body = TRANSITIONS[anchor][step - 1]
    else:
        kind, x, y = BODIES[anchor]
        _, next_x, next_y = BODIES[following]
        body = (kind, x + (next_x - x) * step // 4, y + (next_y - y) * step // 4)
    _draw_celestial_body(canvas, body, horizon)
    windows = blend(distant, horizon, 1, 4)
    if light:
        windows = blend(horizon, (248, 177, 100), 2, 3)
    draw_skyline(canvas, HORIZON_Y, distant, brick, windows)
    if light:
        return INK, (20, 17, 34)
    return (18, 30, 49), blend(middle, (255, 239, 219), 2, 3)
