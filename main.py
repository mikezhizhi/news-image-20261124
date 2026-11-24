#!/usr/bin/env python3
"""news-image-20261124 entry (Python 3.13, standard library only).

The picture of the day is entry.png beside this file. The program
copies those exact bytes to the output directory as entry.png, so
both grading runs write identical output. No network, no clock,
no randomness. The image itself is drawn by draw_news.py.

Local check:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(PICTURE, target)
    if target.stat().st_size != PICTURE.stat().st_size:
        raise SystemExit("size mismatch after copy")
    if target.read_bytes() != PICTURE.read_bytes():
        raise SystemExit("bytes mismatch after copy")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
