import time
from pathlib import Path

import mido  # type: ignore


def second2tick(second: float) -> int:
    return mido.second2tick(second, ticks_per_beat=480, tempo=500000)


def gen_filename(out_dir: str) -> Path:
    return Path(out_dir).expanduser() / "{}.mid".format(int(time.time()))
