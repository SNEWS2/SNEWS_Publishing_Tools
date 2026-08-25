"""Tests for dev/prod broker mode switching."""

import os

import pytest

from snews_pt import snews_pt_utils


@pytest.fixture
def broker_env_files(tmp_path, monkeypatch):
    user_env = tmp_path / "user-config.env"
    dev_env = tmp_path / "dev-config.env"
    prod_env = tmp_path / "prod-config.env"

    user_env.write_text(
        "\n".join(
            [
                "DETECTOR_NAME='LZ'",
                "HAS_NAME_CHANGED='1'",
                "BROKER_MODE='dev'",
                "ADMIN_PASS='secret'",
                "ALERT_OUTPUT='SNEWS_ALERTS/'",
            ]
        )
        + "\n"
    )
    dev_env.write_text(
        "\n".join(
            [
                'HOP_BROKER="kafka.scimma.org"',
                'OBSERVATION_TOPIC="kafka://${HOP_BROKER}/snews.experiments-test"',
                'ALERT_TOPIC="kafka://${HOP_BROKER}/snews.alert-test"',
                'FIREDRILL_OBSERVATION_TOPIC="kafka://${HOP_BROKER}/snews.experiments-firedrill"',
                'FIREDRILL_ALERT_TOPIC="kafka://${HOP_BROKER}/snews.alert-firedrill"',
                'CONNECTION_TEST_TOPIC="kafka://${HOP_BROKER}/snews.connection-testing"',
            ]
        )
        + "\n"
    )
    prod_env.write_text(
        "\n".join(
            [
                'HOP_BROKER="kafka.scimma.org"',
                'OBSERVATION_TOPIC="kafka://${HOP_BROKER}/snews2-exp.experiments"',
                'ALERT_TOPIC="kafka://${HOP_BROKER}/snews2.alert"',
                'FIREDRILL_OBSERVATION_TOPIC="kafka://${HOP_BROKER}/snews2-exp.experiments-firedrill"',
                'FIREDRILL_ALERT_TOPIC="kafka://${HOP_BROKER}/snews2.alert-firedrill"',
                'CONNECTION_TEST_TOPIC="kafka://${HOP_BROKER}/snews2-exp.connection-testing"',
            ]
        )
        + "\n"
    )

    monkeypatch.setattr(snews_pt_utils, "USER_ENV_PATH", str(user_env))
    monkeypatch.setattr(snews_pt_utils, "DEV_ENV_PATH", str(dev_env))
    monkeypatch.setattr(snews_pt_utils, "PROD_ENV_PATH", str(prod_env))
    return user_env, dev_env, prod_env


def test_default_env_path_uses_dev(broker_env_files):
    assert snews_pt_utils.get_broker_mode() == "dev"
    assert snews_pt_utils.default_env_path() == snews_pt_utils.DEV_ENV_PATH


def test_default_env_path_uses_prod(broker_env_files):
    user_env, _, _ = broker_env_files
    user_env.write_text(user_env.read_text().replace("BROKER_MODE='dev'", "BROKER_MODE='prod'"))

    assert snews_pt_utils.get_broker_mode() == "prod"
    assert snews_pt_utils.default_env_path() == snews_pt_utils.PROD_ENV_PATH


def test_set_env_loads_prod_topics(broker_env_files):
    user_env, _, _ = broker_env_files
    user_env.write_text(user_env.read_text().replace("BROKER_MODE='dev'", "BROKER_MODE='prod'"))

    snews_pt_utils.set_env()

    assert os.getenv("DETECTOR_NAME") == "LZ"
    assert os.getenv("OBSERVATION_TOPIC") == "kafka://kafka.scimma.org/snews2-exp.experiments"
    assert os.getenv("ALERT_TOPIC") == "kafka://kafka.scimma.org/snews2.alert"


def test_set_broker_mode_persists_and_preserves_detector_name(broker_env_files):
    snews_pt_utils.set_broker_mode("prod", _return=True)

    assert snews_pt_utils.get_broker_mode() == "prod"
    assert os.getenv("DETECTOR_NAME") == "LZ"
    assert os.getenv("HAS_NAME_CHANGED") == "1"
