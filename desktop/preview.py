"""Draw the shared dashboard in a native Pygame window."""

import argparse
from time import localtime

import pygame

from hub.dashboard import HEIGHT, WIDTH, render


class PygameCanvas:
    def __init__(self, surface):
        self.surface = surface

    def fill_rect(self, x, y, width, height, color):
        self.surface.fill(color, (x, y, width, height))


def main():
    parser = argparse.ArgumentParser(description="N-Gage Hub desktop preview")
    parser.add_argument("--scale", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()
    window_size = (WIDTH * args.scale, HEIGHT * args.scale)

    pygame.display.init()
    try:
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("N-Gage Hub")
        frame = pygame.Surface((WIDTH, HEIGHT)).convert(window)
        canvas = PygameCanvas(frame)
        frame_clock = pygame.time.Clock()
        first_frame = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            render(canvas, localtime())
            pygame.transform.scale(frame, window_size, window)
            pygame.display.flip()
            if first_frame:
                print(f"Preview ready ({pygame.display.get_driver()}, {WIDTH}x{HEIGHT}, "
                      f"{args.scale}x zoom).", flush=True)
                first_frame = False
            frame_clock.tick(30)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.display.quit()


if __name__ == "__main__":
    main()
