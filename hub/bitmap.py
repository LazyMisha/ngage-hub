"""Draw indexed pixel art using horizontal runs of one color."""


def draw_bitmap(canvas, x, y, rows, palette, scale):
    row_index = 0
    for row in rows:
        top = int(row_index * scale)
        bottom = int((row_index + 1) * scale)
        start = 0
        while start < len(row):
            pixel = row[start]
            end = start + 1
            while end < len(row) and row[end] == pixel:
                end += 1
            if pixel in palette:
                left = int(start * scale)
                right = int(end * scale)
                canvas.fill_rect(x + left, y + top, right - left, bottom - top,
                                 palette[pixel])
            start = end
        row_index += 1
