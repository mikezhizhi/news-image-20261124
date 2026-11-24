#!/usr/bin/env python3
"""Copy the finished front page to the output directory.

The entry for news-image-20261124 is the picture entry.png next to
this file, drawn by draw_news.py. This program only copies it to
$MAKEFUN_OUTPUT_DIR/entry.png, byte for byte, so the two grading
runs produce identical output. Standard library only.

Check it locally:
    python3 main.py   # with MAKEFUN_OUTPUT_DIR set, else /output
"""

import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def run():
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "entry.png"
    shutil.copyfile(SOURCE, destination)
    written = destination.read_bytes()
    original = SOURCE.read_bytes()
    if written != original:
        raise SystemExit("output differs from entry.png")
    print("wrote {} ({} bytes)".format(destination, len(written)))


if __name__ == "__main__":
    run()
