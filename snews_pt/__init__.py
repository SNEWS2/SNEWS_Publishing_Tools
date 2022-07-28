try:
    from ._version import version as __version__
except ImportError:
    pass

import os, click
import warnings
import dotenv
from dotenv import load_dotenv
envpath = os.path.join(os.path.dirname(__file__), 'auxiliary/test-config.env')
load_dotenv(envpath)

from .snews_pt_utils import retrieve_detectors
import click
detectors = list(retrieve_detectors().keys())
if int(os.getenv("HAS_NAME_CHANGED")) == 0:
    warning_text = click.style('You are using default detector name "TEST"\n'
                               'Please change this by snews_pt.snews_pt_utils.set_name()',
                               fg='red')
    warnings.warn(warning_text, UserWarning)

