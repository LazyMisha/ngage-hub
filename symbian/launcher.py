"""Full-screen clock for the PyS60 1.3.1 script shell."""

import appuifw
import e32
import graphics
import imp
import os
import sys
from time import localtime

from hub.dashboard import COLON_REGION, HEIGHT, WIDTH, draw_colon, render


def keep_awake_callback(helper):
    reset = getattr(e32, "reset_inactivity", None)
    if reset is not None:
        return reset

    # PyS60 1.3.1 lacks the API. Cache the bundled EKA1 extension on the
    # Python drive, or in phone memory if the MMC is read-only.
    directory = os.path.dirname(appuifw.app.full_name())
    paths = (os.path.join(directory, "_ngageawake_v1.pyd"),
             u"c:\\system\\_ngageawake_v1.pyd")
    for path in paths:
        try:
            try:
                source = open(path, "rb")
            except IOError:
                source = open(path, "wb")
                try:
                    source.write(helper)
                finally:
                    source.close()
            else:
                try:
                    if source.read(len(helper) + 1) != helper:
                        continue
                finally:
                    source.close()
            return imp.load_dynamic("_ngageawake", path).reset
        except (IOError, OSError, ImportError):
            continue
    return None


class PhoneClock:
    def __init__(self, reset_inactivity):
        self.image = graphics.Image.new((WIDTH, HEIGHT))
        x, y, width, height = COLON_REGION
        self.colon_background = graphics.Image.new((width, height))
        self.colon_source = ((x, y), (x + width, y + height))
        self.canvas = None
        self.minute = None
        self.second = None
        self.lock = e32.Ao_lock()
        self.timer = e32.Ao_timer()
        self.error = None
        self.reset_inactivity = reset_inactivity
        self.running = False

    def fill_rect(self, x, y, width, height, color):
        self.image.rectangle((x, y, x + width, y + height), outline=None, fill=color)

    def redraw(self, rect):
        if self.canvas is not None and self.minute is not None:
            size = self.canvas.size
            if size == (WIDTH, HEIGHT):
                self.canvas.blit(self.image)
            else:
                self.canvas.blit(self.image, target=((0, 0), size), scale=1)

    def refresh(self):
        now = localtime()
        minute = now[:5]
        if self.minute == minute and self.second == now[5]:
            return
        x, y, width, height = COLON_REGION
        new_minute = self.minute != minute
        if new_minute:
            self.ink, self.shadow = render(self, now, animate_colon=False)
            self.colon_background.blit(self.image, source=self.colon_source)
        self.minute, self.second = minute, now[5]
        if self.second % 2 == 0:
            draw_colon(self, self.ink, self.shadow)
        else:
            self.image.blit(self.colon_background, target=(x, y))
        if new_minute or self.canvas.size != (WIDTH, HEIGHT):
            self.redraw(None)
        else:
            self.canvas.blit(self.image, target=(x, y), source=self.colon_source)

    def tick(self):
        if not self.running:
            return
        try:
            if self.reset_inactivity is not None:
                self.reset_inactivity()
            self.refresh()
            self.timer.after(1, self.tick)
        except Exception:
            self.error = sys.exc_info()[1]
            self.stop()

    def stop(self):
        if self.running:
            self.running = False
            self.timer.cancel()
            self.lock.signal()

    def run(self):
        app = appuifw.app
        previous_screen = app.screen
        previous_body = app.body
        previous_exit = app.exit_key_handler
        try:
            if self.reset_inactivity is None:
                appuifw.note(u"The clock can run, but keep-awake is unavailable.", "info")
            app.screen = "full"
            self.canvas = appuifw.Canvas(redraw_callback=self.redraw)
            app.body = self.canvas
            app.exit_key_handler = self.stop
            self.running = True
            self.tick()
            self.lock.wait()
            if self.error is not None:
                raise self.error
        finally:
            self.running = False
            self.timer.cancel()
            self.canvas = None
            app.body = previous_body
            app.screen = previous_screen
            app.exit_key_handler = previous_exit


def main(helper):
    PhoneClock(keep_awake_callback(helper)).run()
