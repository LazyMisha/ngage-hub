"""Draw indexed pixel art using horizontal runs of one color."""


def draw_bitmap(canvas, x, y, rows, palette, scale):
    for row in rows:
        start = 0
        while start < len(row):
            pixel = row[start]
            end = start + 1
            while end < len(row) and row[end] == pixel:
                end += 1
            if pixel in palette:
                canvas.fill_rect(x + start * scale, y,
                                 (end - start) * scale, scale, palette[pixel])
            start = end
        y += scale
