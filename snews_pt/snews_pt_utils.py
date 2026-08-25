"""
Utility tools for snews_pt
"""

import json
import os
from collections import namedtuple

import click
import dotenv
from dotenv import load_dotenv

from .core.logging import getLogger

log = getLogger(__name__)
default_detector_file = (
    os.path.dirname(__file__) + "/auxiliary/detector_properties.json"
)

AUX_DIR = os.path.join(os.path.dirname(__file__), "auxiliary")
USER_ENV_PATH = os.path.join(AUX_DIR, "user-config.env")
DEV_ENV_PATH = os.path.join(AUX_DIR, "dev-config.env")
PROD_ENV_PATH = os.path.join(AUX_DIR, "prod-config.env")
BROKER_MODES = ("dev", "prod")


def get_broker_mode():
    """Return the persisted broker profile (dev or prod)."""
    values = dotenv.dotenv_values(USER_ENV_PATH)
    mode = (values.get("BROKER_MODE") or "dev").strip("'\"")
    if mode not in BROKER_MODES:
        return "dev"
    return mode


def default_env_path():
    """Return the path to the active bundled topic environment file."""
    if get_broker_mode() == "prod":
        return PROD_ENV_PATH
    return DEV_ENV_PATH


def _load_broker_profile():
    """Load user settings, then topic vars for the active broker mode."""
    load_dotenv(USER_ENV_PATH, override=True)
    topic_path = PROD_ENV_PATH if get_broker_mode() == "prod" else DEV_ENV_PATH
    load_dotenv(topic_path, override=True)


def resolve_env_path(env_path=None):
    """Resolve an environment file path for loading.

    Parameters
    ----------
    env_path : str, optional
        Path supplied by the user. If omitted, the bundled default is used.
        Relative paths are resolved against the current working directory.
        Absolute paths and ``~`` are accepted as-is (after expansion).

    Returns
    -------
    str
        Absolute path to the environment file.

    """
    if not env_path:
        return default_env_path()

    env_path = os.path.expanduser(env_path)

    # Backward compatibility: "/auxiliary/..." was historically package-relative.
    if env_path.startswith("/auxiliary/"):
        legacy_path = os.path.join(os.path.dirname(__file__), env_path.lstrip("/"))
        if os.path.isfile(legacy_path):
            return legacy_path

    return os.path.abspath(env_path)


def set_env(env_path=None):
    """Set environment parameters

    Parameters
    ----------
    env_path : str, (optional)
        path for the environment file.
        Use default settings if not given

    """
    if env_path is None:
        _load_broker_profile()
        return

    load_dotenv(resolve_env_path(env_path), override=True)


def set_broker_mode(mode, _return=False):
    """Switch between dev and production topic profiles.

    Parameters
    ----------
    mode : str
        Either ``dev`` or ``prod``.
    _return : bool, optional
        If True, return the active broker mode instead of printing feedback.

    """
    if mode not in BROKER_MODES:
        raise ValueError(f"broker mode must be one of {BROKER_MODES}, got {mode!r}")

    set_env()
    dotenv.set_key(USER_ENV_PATH, "BROKER_MODE", mode)
    set_env()

    if _return:
        return mode

    click.secho(f"Broker mode set to: {mode}", fg="green", bold=True)
    click.secho(f"  Observation: {os.getenv('OBSERVATION_TOPIC')}")
    click.secho(f"  Alert: {os.getenv('ALERT_TOPIC')}")


def retrieve_detectors(detectors_path=default_detector_file):
    """Retrieve the name-ID-location of the participating detectors.

    Parameters
    ----------
    detectors_path : str, optional
        path to detector properties. File needs to be in JSON format

    Returns
    -------
    None

    """
    if not os.path.isfile(detectors_path):
        os.system(f"python {os.path.dirname(__file__)}/auxiliary/make_detector_file.py")

    with open(detectors_path) as json_file:
        detectors = json.load(json_file)

    # make a namedtuple
    Detector = namedtuple("Detector", ["name", "id", "location"])
    for k, v in detectors.items():
        detectors[k] = Detector(v[0], v[1], v[2])
    return detectors


def isnotebook():
    """Tell if the script is running on a notebook"""
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def display_gif():
    """Some fun method to display an alert gif
    If running on notebook.

    """
    if isnotebook():
        from IPython.display import HTML, display

        giphy_snews = (
            "https://raw.githubusercontent.com/SNEWS2/"
            "hop-SNalert-app/snews2_dev/hop_comms/auxiliary/snalert.gif"
        )
        display(HTML(f"<img src={giphy_snews}>"))


def set_name(detector_name="TEST", _return=False):
    """set your detector's name.
    Messages sent with detector_name="TEST" will be ignored at the server
    Alerts can still be subscribed and listened as "TEST"

    """

    load_dotenv(USER_ENV_PATH)
    detectors = list(retrieve_detectors().keys())
    if detector_name == "TEST":
        if int(os.getenv("HAS_NAME_CHANGED")) == 0:
            for i, d in enumerate(detectors):
                click.secho(f"[{i:2d}] {d}")
            inp = input(
                click.secho("Please put select your detector's index\n", bold=True)
            )
            detector_name = detectors[int(inp)]
            os.environ["DETECTOR_NAME"] = detector_name
            os.environ["HAS_NAME_CHANGED"] = "1"
            dotenv.set_key(USER_ENV_PATH, "DETECTOR_NAME", os.environ["DETECTOR_NAME"])
            dotenv.set_key(USER_ENV_PATH, "HAS_NAME_CHANGED", os.environ["HAS_NAME_CHANGED"])
        else:
            detector_name = os.environ["DETECTOR_NAME"]
    else:
        if detector_name not in detectors:
            raise KeyError(
                f"{detector_name} is not a valid detector. \nChoose from {detectors}"
            )
        os.environ["DETECTOR_NAME"] = detector_name
        os.environ["HAS_NAME_CHANGED"] = "1"
        dotenv.set_key(USER_ENV_PATH, "DETECTOR_NAME", os.environ["DETECTOR_NAME"])
        dotenv.set_key(USER_ENV_PATH, "HAS_NAME_CHANGED", os.environ["HAS_NAME_CHANGED"])
    if _return:
        return detector_name
    else:
        click.secho(f'You are {os.environ["DETECTOR_NAME"]}')
