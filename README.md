# N-Gage Hub

A 176 × 208 pixel-art clock and date over the Łódź skyline. The sky switches among twelve scenes every two hours, starting at midnight. The clock, date, and scene follow your Mac's local time. The 18:00–19:59 slot shows the original orange sunset.

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

Press **Esc** or close the window to quit. Saving a Python file under `hub/` or `desktop/` restarts the preview. If a save causes a Python error, the terminal shows the traceback and watches for your next save. Restart the dev command itself after editing `desktop/dev.py`.

The preview opens at 176 × 208 by default. Add `--scale 2` for 2× zoom. The range is 1×–5×. For a one-off preview, run `.venv/bin/python -B -m desktop.preview`.

## Edit the dashboard

| File | What to change |
| --- | --- |
| `hub/dashboard.py` | Clock layout and optional weather artwork |
| `hub/day_cycle.py` | Two-hour sky scenes, celestial bodies, and clock colors |
| `hub/sunset.py` | Shared skyline and original sunset |
| `hub/pixel_font.py` | Bitmap glyphs and text sizing |
| `hub/mock_weather.py` | City label and offline weather samples |
| `desktop/preview.py` | Pygame window, keyboard controls, scaling, and frame timing |
| `desktop/dev.py` | File watching and preview restarts |
| `symbian/launcher.py` | Full-screen PyS60 clock and redraw timer |
| `symbian/build.py` | Builds the single script to transfer to the phone |

The shared `hub/` package uses ASCII source, Python 2.2-era syntax, and no platform or third-party imports. The desktop preview calls `hub.dashboard.render(canvas, local_time)` with the tuple fields from `time.localtime()`. For weather development, the renderer also accepts a sample from `hub/mock_weather.py` and integer milliseconds since the animation began. The canvas implements `fill_rect(x, y, width, height, color)` using integer coordinates and an RGB tuple. The rectangle spans `width` by `height` pixels starting at `(x, y)`. The renderer paints a full frame. The desktop adapter scales that frame with nearest-neighbor sampling.

## Run on an N-Gage

Start with the **N-Gage QD**. Nokia's setup guide lists the QD under S60 1st Edition FP1. This launcher targets **PyS60 1.3.1 for 1st Edition**, based on Python 2.2.2. The original N-Gage Classic needs a separate firmware and runtime check. The dashboard has yet to be tested on a physical handset or a Symbian emulator. [Nokia's setup guide](https://www.mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf) · [Nokia's PyS60 1.3.1 reference](https://mobilenin.com/pys60/resources/pys60_v_1_3_1/PythonForS60_doc_1_3_1.pdf)

1. Download `PythonForS60_1stEd_1_3_1.SIS` from the 1.3.1 release archive. Pair the QD with your Mac, then use **Bluetooth File Exchange** to send the installer. On the QD, open the received file in **Messaging → Inbox** and install it. [PyS60 1.3.1 release archive](https://sourceforge.net/projects/pys60/files/pys60/1.3.1/) · [Apple's file-transfer instructions](https://support.apple.com/en-euro/guide/mac-help/mchle7fa9e15/mac)
2. From the project directory on the Mac, run `python3 symbian/build.py`. This writes `build/ngage_hub.py`, which contains the full clock, city label, and twelve backgrounds.
3. Send `ngage_hub.py` to the QD the same way. Open it in the Inbox and choose **Python script** when asked where to install it. From the main menu, open **Python → Options → Run script** and select `ngage_hub.py`. [Nokia's script installation instructions](https://mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf#page=14)
4. The clock uses the phone's date and time. Press the **right softkey** to return to Python.

If Bluetooth transfer is unavailable, use a writable MMC and a reader that supports MMC cards. Copy the SIS to the card and install it from **Tools → Manager**. Choose the memory card as the install location. Place the script under `System/Apps/Python/my/` on that card and select it from **Run script**. The script folder should be on the drive where PyS60 is installed. [Nokia's QD user guide](https://i.smartphone.ua/docs/instr/Nokia_N_Gage_QD_UG_en.pdf) · [Nokia's script installation instructions](https://mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf#page=14)

On first launch, check that the screen fills all 176 × 208 pixels, the date and time agree with the handset, and the right softkey returns to Python. Switch away and back to check redraw. If the launcher reports another canvas size, or Python shows an error, record the exact message and the phone model and firmware.
