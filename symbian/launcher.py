"""Full-screen clock for the PyS60 1.3.1 script shell."""

import appuifw
import e32
import graphics
import sys
from time import localtime

from hub.dashboard import HEIGHT, WIDTH, render


class PhoneClock:
    def __init__(self):
        self.image = graphics.Image.new((WIDTH, HEIGHT))
        self.canvas = None
        self.minute = None
        self.lock = e32.Ao_lock()
        self.timer = e32.Ao_timer()
        self.error = None

    def fill_rect(self, x, y, width, height, color):
        self.image.rectangle((x, y, x + width, y + height), outline=None, fill=color)

    def redraw(self, rect):
        if self.canvas is not None and self.minute is not None:
            self.canvas.blit(self.image)

    def refresh(self):
        now = localtime()
        minute = now[:5]
        if self.minute != minute:
            render(self, now)
            self.minute = minute
            self.redraw(None)

    def tick(self):
        try:
            self.refresh()
            self.timer.after(1, self.tick)
        except Exception:
            self.error = sys.exc_info()[1]
            self.stop()

    def stop(self):
        self.timer.cancel()
        self.lock.signal()

    def run(self):
        app = appuifw.app
        previous_screen = app.screen
        previous_body = app.body
        previous_exit = app.exit_key_handler
        try:
            app.screen = "full"
            self.canvas = appuifw.Canvas(redraw_callback=self.redraw)
            app.body = self.canvas
            if self.canvas.size != (WIDTH, HEIGHT):
                message = u"N-Gage Hub needs 176 x 208. Canvas is %d x %d."
                appuifw.note(message % self.canvas.size, "error")
                return
            app.exit_key_handler = self.stop
            self.refresh()
            self.timer.after(1, self.tick)
            self.lock.wait()
            if self.error is not None:
                raise self.error
        finally:
            self.timer.cancel()
            self.canvas = None
            app.body = previous_body
            app.screen = previous_screen
            app.exit_key_handler = previous_exit


def main():
    PhoneClock().run()
