# read the config file supplied as the first argument and write the associated
# files to stdout, if they exist

import logging
import sys
from pathlib import Path

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("get_files.py")


def maybe_print(path):
    if Path(path).exists():
        print(path)
    else:
        logger.warning(f"skipping non-existent file: {path}")


conf = Config.from_file(sys.argv[1])
maybe_print(conf.forcefield)
for ds in conf.datasets:
    maybe_print(ds)
