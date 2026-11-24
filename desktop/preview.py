"""Draw the shared dashboard in a native Pygame window."""

import argparse
from time import localtime, monotonic

import pygame

from hub.dashboard import HEIGHT, WIDTH, render
from hub.mock_weather import SAMPLES


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
        pygame.display.set_caption("N-Gage Hub | Space: weather | Esc: quit")
        frame = pygame.Surface((WIDTH, HEIGHT)).convert(window)
        canvas = PygameCanvas(frame)
        frame_clock = pygame.time.Clock()
        sample = 0
        started = monotonic()
        first_frame = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        sample = (sample + 1) % len(SAMPLES)
                        started = monotonic()

            elapsed_ms = int((monotonic() - started) * 1000)
            render(canvas, localtime(), SAMPLES[sample], elapsed_ms)
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
