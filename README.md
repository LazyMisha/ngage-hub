# N-Gage Hub

A 176 × 208 pixel-art weather and clock dashboard inspired by the Nokia N-Gage Classic and QD. The preview uses your Mac's local time and shows offline demo weather for Łódź. The weather card animates drifting clouds, falling rain, or pulsing sunshine.

## Run on a Mac

Use Python 3.11–3.14. From the project directory, set up the virtual environment once.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Start the preview with live reload.

```sh
.venv/bin/python -B -m desktop.dev
```

Press **Space** to switch between weather samples and **Esc** to close the preview. The watcher checks Python files under `hub/` and `desktop/` five times per second. Saving a file starts a fresh preview window and resets it to the default sample. If a save causes a Python error, the terminal shows the traceback and watches for your next save. Restart the dev command itself after editing `desktop/dev.py`.

Add `--scale 2` for 2× zoom. The range is 1×–5×, with 3× as the default. For a one-off preview, run `.venv/bin/python -B -m desktop.preview`.

## Edit the dashboard

| File | What to change |
| --- | --- |
| `hub/dashboard.py` | Layout, colors, weather sprites, and animation |
| `hub/pixel_font.py` | Bitmap glyphs and text sizing |
| `hub/mock_weather.py` | Demo city, conditions, and temperatures in Celsius |
| `desktop/preview.py` | Pygame window, keyboard controls, scaling, and frame timing |
| `desktop/dev.py` | File watching and preview restarts |

The shared `hub/` package uses ASCII source, Python 2.2-era syntax, and no platform or third-party imports. The entry point is `hub.dashboard.render(canvas, local_time, weather, elapsed_ms)`. Pass the tuple fields from `time.localtime()`, a weather sample with the same fields as the demo samples, and integer milliseconds since the animation began. The canvas implements `fill_rect(x, y, width, height, color)` using integer coordinates and an RGB tuple. The rectangle spans `width` by `height` pixels starting at `(x, y)`. The renderer paints a full frame. The desktop adapter scales that frame with nearest-neighbor sampling.

## Symbian port and device validation

This MVP runs on the Mac. The PyS60 adapter and phone packaging are future work. Shared code targets the Python 2.2 language subset for portability. Runtime execution on Python 2.2 or on a handset is unverified.

1. Record the exact model and firmware for each handset. Nokia's PyS60 1.2 guide identifies the 1st Edition FP1 package for the N-Gage QD and Python 2.2.2 as the interpreter. Check the Classic independently. [Nokia's PyS60 1.2 getting-started guide](https://www.mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf)
2. On each handset, run a minimal shell script to confirm the interpreter and imports for `appuifw`, `graphics`, and `e32`. Open a full-screen canvas and measure the usable pixel area. Draw at the four corners to check clipping and orientation.
3. Add a Symbian entry point outside `hub/`. Implement `fill_rect` on a `graphics.Image` buffer and blit on canvas redraw. Verify whether the rectangle API includes its ending coordinates. Use an `e32` timer to schedule updates and bind an available keypad key for cycling samples. [Nokia's graphics and UI examples](https://www.mobilenin.com/pys60/resources/pys60_v_1_2/Programming_with_Python.pdf)
4. Run the shared dashboard with the demo samples. Confirm text legibility, colors, redraw after focus or backlight changes, sample switching, and a clean exit. Start around 5–10 FPS and measure responsiveness and memory on each model before tuning.

The demo requires no weather API, credentials, Bluetooth, or data service.
