"""Pixel-art sky and skyline painted with integer rectangles."""

SKYLINE_BASE = 113
SUNSET_GROUND = (45, 11, 5)

SKY = (
    (0, (54, 13, 17)),
    (33, (103, 24, 26)),
    (48, (119, 27, 25)),
    (62, (170, 38, 23)),
    (79, (222, 57, 18)),
    (93, (242, 75, 12)),
    (102, (255, 119, 10)),
    (113, (230, 79, 7)),
)

STREAKS = (
    (0, 39, 27, 2, (149, 34, 22)),
    (0, 42, 18, 2, (179, 41, 21)),
    (157, 42, 19, 2, (172, 39, 22)),
    (0, 59, 29, -1, (182, 45, 22)),
    (130, 67, 46, 2, (204, 50, 15)),
    (150, 73, 26, 2, (221, 57, 15)),
    (0, 70, 46, -1, (226, 65, 18)),
    (0, 74, 28, -1, (244, 75, 20)),
    (111, 96, 65, 2, (254, 100, 9)),
    (104, 100, 72, 1, (255, 130, 12)),
    (21, 91, 63, -1, (226, 61, 13)),
    (32, 100, 81, 0, (253, 104, 11)),
    (41, 104, 80, 0, (255, 112, 11)),
)

ROOFS = (
    (32, 14, 106), (46, 15, 104), (51, 2, 101), (55, 2, 101),
    (64, 17, 106), (69, 2, 105), (73, 2, 105), (81, 9, 107),
    (96, 8, 108), (99, 10, 106), (104, 6, 104), (106, 6, 102),
    (112, 6, 104), (118, 12, 106), (126, 3, 105), (130, 5, 107),
    (148, 14, 106), (151, 8, 101), (163, 2, 99), (159, 17, 102),
    (167, 3, 79), (172, 4, 98),
)


def blend(first, last, step, steps):
    return (
        first[0] + (last[0] - first[0]) * step // steps,
        first[1] + (last[1] - first[1]) * step // steps,
        first[2] + (last[2] - first[2]) * step // steps,
    )


def draw_sky(canvas, width, horizon, colors):
    source_horizon = colors[-1][0]
    for band in range(len(colors) - 1):
        top, first = colors[band]
        bottom, last = colors[band + 1]
        top = top * horizon // source_horizon
        bottom = bottom * horizon // source_horizon
        for y in range(top, bottom):
            canvas.fill_rect(0, y, width, 1, blend(first, last, y - top, bottom - top))


def draw_sunset(canvas, width, horizon=SKYLINE_BASE):
    draw_sky(canvas, width, horizon, SKY)
    offset = horizon - SKYLINE_BASE
    for x, y, span, rise, color in STREAKS:
        for piece in range(4):
            start = span * piece // 4
            end = min(span, span * (piece + 1) // 4 + 4)
            streak_y = (y - rise * piece) * horizon // SKYLINE_BASE
            canvas.fill_rect(x + start, streak_y, end - start, 2, color)

    widths = (5, 9, 13, 15, 17, 19, 19, 19, 19, 17, 15, 11, 7, 3)
    for row in range(len(widths)):
        color = (255, 218, 98)
        if row in (6, 7, 10):
            color = (246, 154, 25)
        span = widths[row]
        canvas.fill_rect(139 - span // 2, offset + 95 + row, span, 1, color)

    draw_skyline(canvas, horizon, (66, 18, 15), (52, 13, 9), (169, 46, 14))


def draw_skyline(canvas, horizon, distant, brick, windows):
    offset = horizon - SKYLINE_BASE
    for x, span, top in ROOFS:
        canvas.fill_rect(x, offset + top, span, SKYLINE_BASE - top, distant)

    # The foreground roof and chimney suggest Lodz's old textile mills.
    canvas.fill_rect(0, offset + 81, 8, 32, brick)
    canvas.fill_rect(8, offset + 83, 12, 30, brick)
    canvas.fill_rect(16, offset + 80, 3, 19, brick)
    canvas.fill_rect(15, offset + 81, 6, 1, brick)
    canvas.fill_rect(20, offset + 92, 6, 21, brick)
    canvas.fill_rect(26, offset + 94, 9, 19, brick)
    canvas.fill_rect(35, offset + 96, 6, 17, brick)
    canvas.fill_rect(37, offset + 93, 2, 5, brick)
    for x in (8, 11, 14):
        canvas.fill_rect(x, offset + 87, 1, 3, windows)
    canvas.fill_rect(10, offset + 98, 3, 1, windows)
    canvas.fill_rect(8, offset + 100, 7, 7, windows)
    canvas.fill_rect(11, offset + 98, 1, 9, brick)
    canvas.fill_rect(8, offset + 103, 7, 1, brick)
    for x in (20, 24, 28, 32, 36):
        canvas.fill_rect(x, offset + 100, 2, 7, windows)
        canvas.fill_rect(x, offset + 103, 2, 1, brick)
