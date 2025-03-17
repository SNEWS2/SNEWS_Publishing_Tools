"""
Modified version of Geoffrey Letner's python 201 logger.

Ref: https://python-tutorial.dev/201/tutorial/logging.html
"""

import os
import time
from datetime import date
from socket import gethostname
from logging import (
    getLogger,
    NullHandler,
    Formatter,
    FileHandler,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)

HOST = gethostname()

log_date = date.today().strftime("%Y-%m-%d")
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../logs")
log_file = f"{log_dir}/{log_date}.log"

if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

fh = FileHandler(log_file)

formatter = Formatter(
    f"%(asctime)s on {HOST}\n" f"  %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y/%m/%dT%H:%M:%S.f",
)

formatter.converter = time.gmtime

fh.setFormatter(formatter)

logger = getLogger("snews_pt")
logger.addHandler(NullHandler())

levels = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR,
    "critical": CRITICAL,
}


def initialize_logging(level):
    """Initialize top-level logger with the file handler and a `level`."""
    if fh not in logger.handlers:
        logger.addHandler(fh)
        logger.setLevel(levels.get(level))
        logger.propagate = False
