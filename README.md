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

## Run on the original Nokia N-Gage (Classic)

The original Nokia N-Gage (NEM-4) uses Series 60. The included PyS60 1.3.1 installer declares the general Series 60 product ID. This is the installer to try first on the Classic. Installation and dashboard operation still need to be verified on the handset. [Nokia N-Gage user guide](https://db.hfsplay.fr/files/2019/09/11/nokia-n-gage_O75pEQx.pdf) · [Series 60 product IDs](https://docs.huihoo.com/symbian/s60-5th-edition-cpp-developers-library-v2.1/GUID-35228542-8C95-4849-A73F-2B4F082F0C44/sdk/doc_source/faqSDK/faq_1045.html)

1. Copy the included [`PythonForS60_1stEd_1_3_1.SIS`](symbian/PythonForS60_1stEd_1_3_1.SIS) to the root of a writable MMC. Use the Classic's mini-USB data cable if the card appears in Finder, or use a reader that supports MMC. Eject the card in Finder and disconnect the cable before opening the card on the phone. [Nokia's USB and installation instructions](https://db.hfsplay.fr/files/2019/09/11/nokia-n-gage_O75pEQx.pdf)
2. On the Classic, open **Menu → Tools → Manager**, select the SIS, and choose **Options → Install**. Pick **Memory card** if prompted so you can transfer the dashboard over USB or a card reader. After installation, check that **Python** opens from the main menu. [Nokia's installation instructions](https://db.hfsplay.fr/files/2019/09/11/nokia-n-gage_O75pEQx.pdf)
3. If you installed PyS60 on the MMC, copy the included [`ngage_hub.py`](symbian/ngage_hub.py) into `System/Apps/Python/my/` on the card, creating `my` if needed. The script must be on the same drive as PyS60 for the shell to list it there. [Nokia's script installation instructions](https://mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf#page=14)
4. Open **Python → Options → Run script** and select `ngage_hub.py`. The clock uses the Classic's date and time to choose the background. Press the **right softkey** to return to Python.

After editing the dashboard, run `python3 symbian/build.py symbian/ngage_hub.py` from the project directory to refresh the included phone script.

For Bluetooth transfer, pair the Classic with the Mac and use **Bluetooth File Exchange**. Send the SIS first and open it in **Messaging → Inbox** to install. Send `ngage_hub.py` next and choose **Python script** when opening it from the Inbox. Use this method for the script if PyS60 is installed in phone memory. [Apple's Bluetooth transfer instructions](https://support.apple.com/en-euro/guide/mac-help/mchle7fa9e15/mac) · [Nokia's Python setup guide](https://mobilenin.com/pys60/resources/pys60_v_1_2/Getting_Started_with_Python.pdf)

On first launch, check that the dashboard fills the 176 × 208 screen, the date and time match the phone, and the right softkey returns to Python. If installation or launch fails, note the exact message and the Classic's firmware version.
