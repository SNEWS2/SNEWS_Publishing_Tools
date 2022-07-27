try:
    from ._version import version as __version__
except ImportError:
    pass

import os
import dotenv
from dotenv import load_dotenv
envpath = os.path.join(os.path.dirname(__file__), 'auxiliary/test-config.env')
load_dotenv(envpath)

from .snews_pt_utils import retrieve_detectors
import click
detectors = list(retrieve_detectors().keys())
if int(os.getenv("HAS_NAME_CHANGED")) == 0:
    for i,d in enumerate(detectors):
        click.secho(f"[{i:2d}] {d}")
    inp = input(click.secho("Please put select your detector's index\n", bold=True))
    selected_name = detectors[int(inp)]
    os.environ["DETECTOR_NAME"] = selected_name
    os.environ["HAS_NAME_CHANGED"] = "1"

    dotenv.set_key(envpath, "DETECTOR_NAME", os.environ["DETECTOR_NAME"])
    dotenv.set_key(envpath, "HAS_NAME_CHANGED", os.environ["HAS_NAME_CHANGED"])


