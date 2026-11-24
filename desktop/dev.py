"""Restart the desktop preview after saved Python edits."""

import signal
import subprocess
import sys
from pathlib import Path
from time import sleep


ROOT = Path(__file__).resolve().parents[1]
WATCHED = (ROOT / "hub", ROOT / "desktop")


def source_snapshot():
    snapshot = {}
    for directory in WATCHED:
        for path in directory.rglob("*.py"):
            try:
                info = path.stat()
            except FileNotFoundError:
                # An editor can replace the file between glob and stat.
                continue
            snapshot[path] = (info.st_mtime_ns, info.st_size, info.st_ino)
    return snapshot


def stop_preview(process):
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def interrupt(_signal, _frame):
    raise KeyboardInterrupt


def main():
    signal.signal(signal.SIGTERM, interrupt)
    command = [sys.executable, "-B", "-m", "desktop.preview", *sys.argv[1:]]
    process = None
    try:
        print("Watching hub/ and desktop/ for changes.", flush=True)
        previous = source_snapshot()
        process = subprocess.Popen(command, cwd=ROOT)
        while True:
            sleep(0.2)
            if process is not None:
                status = process.poll()
                if status == 0:
                    return
                if status is not None:
                    print(f"Preview exited ({status}). Save an edit to retry.", flush=True)
                    process = None
            current = source_snapshot()
            if current != previous:
                previous = current
                print("Reloading preview...", flush=True)
                stop_preview(process)
                process = subprocess.Popen(command, cwd=ROOT)
    except KeyboardInterrupt:
        pass
    finally:
        stop_preview(process)


if __name__ == "__main__":
    main()
