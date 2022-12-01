"""
Easy handle remote commands


Melih Kara, kara@kit.edu
"""

from hop import Stream
from datetime import datetime, timedelta
import os, click, getpass

def test_connection(detector_name=None, firedrill=True, start_at=-5, wait=10):
    """ test the server connection
        It should prompt your whether the
        coincidence script is running in the server
        :param start_at: `negative int` the last N number of msg to check
        :param wait: `int` seconds to wait before terminating the check
    """
    detector_name = detector_name or os.getenv("DETECTOR_NAME")
    stamp_time = datetime.utcnow().isoformat()
    message = {'_id': '0_test-connection',
               'detector_name': detector_name,
               'time': stamp_time,
               'status': 'sending',
               'meta':{}}
    if firedrill:
        topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC")
    else:
        topic = os.getenv("OBSERVATION_TOPIC")
    substream = Stream(until_eos=True, auth=True, start_at=start_at)
    pubstream = Stream(until_eos=True, auth=True)
    click.secho(f"\n> Testing your connection to {topic}. \n> Should take ~10 seconds...\n")

    start_time = datetime.utcnow()
    confirmed = False
    with pubstream.open(topic, "w") as ps, substream.open(topic, "r") as ss:
        ps.write(message)
        while (datetime.utcnow() - start_time) < timedelta(seconds=wait):
            for read in ss:
                message_expected = message.copy()
                message_expected["status"] = "received"
                if read == message_expected:
                    read_name = click.style(read['detector_name'], fg='green', bold=True)
                    read_time = click.style(read['time'], fg='green', bold=True)
                    click.echo(f"You ({read_name}) have a connection to the server at {read_time}")
                    confirmed=True
                    break
                break
            break
    if not confirmed:
        click.secho(f"\tCouldn't get a confirmation in {wait} sec. "
                    f"\n\tMaybe increase timeout and try again.", fg='red', bold=True)


def write_hb_logs(detector_name=None, admin_pass=None, firedrill=True):
    """ REQUIRES AUTHORIZATION
        ask to print the HB logs on the server standard output
        later admins can see them remotely
    """
    passw = admin_pass or os.getenv("ADMIN_PASS", "NO_AUTH")
    detector_name = detector_name or os.getenv("DETECTOR_NAME")
    message = {'_id': '0_display-heartbeats',
               'pass': passw,
               'detector_name':detector_name,
               'meta':{}}
    topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC") if firedrill else os.getenv("OBSERVATION_TOPIC")
    pubstream = Stream(until_eos=True, auth=True)

    with pubstream.open(topic, "w") as ps:
        ps.write(message)
    logslink = "> https://www.physics.purdue.edu/snews/logs/"
    click.secho(f"> Requested logs. If you have rights, go to remote Purdue server logs\n{logslink}\n",
                fg='blue', bold=True)


def reset_cache(detector_name=None, admin_pass=None, firedrill=True):
    """ REQUIRES AUTHORIZATION
        If authorized, drop the current cache at the server
    """
    passw = admin_pass or os.getenv("ADMIN_PASS", "NO_AUTH")
    detector_name = detector_name or os.getenv("DETECTOR_NAME")
    message = {'_id': '0_hard-reset',
               'pass': passw,
               'detector_name':detector_name,
               'meta':{}}

    topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC") if firedrill else os.getenv("OBSERVATION_TOPIC")
    pubstream = Stream(until_eos=True, auth=True)

    with pubstream.open(topic, "w") as ps:
        ps.write(message)
        click.secho(f"> Requesting to Reset the cache. If you have rights, cache will be reset", fg='blue', bold=True)


def change_broker(brokername, detector_name=None, admin_pass=None,firedrill=True):
    """ REQUIRES AUTHORIZATION
        If authorized, server changes the broker
    """
    passw = admin_pass or os.getenv("ADMIN_PASS", "NO_AUTH")
    detector_name = detector_name or os.getenv("DETECTOR_NAME")
    message = {'_id': '0_broker-change',
               'pass': passw,
               'detector_name': detector_name,
               'new_broker':brokername,
               'meta':{}}

    current_topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC") if firedrill else os.getenv("OBSERVATION_TOPIC")
    pubstream = Stream(until_eos=True, auth=True)

    with pubstream.open(current_topic, "w") as ps:
        ps.write(message)
        click.secho(f"> Requesting to change the broker. If you have rights, broker will be changed", fg='blue', bold=True)


def get_feedback(detector_name=None, firedrill=True):
    """ REQUIRES AUTHORIZATION
        Get heartbeat feedback by email
    """
    detector_name = detector_name or os.getenv("DETECTOR_NAME")
    email_address = input("Your registered email address: ")
    pswd = getpass.getpass('Password:')
    message = {'_id': '0_Get-Feedback',
               'email': email_address,
               'pass': pswd,
               'detector_name': detector_name,
               'meta': {}}
    topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC") if firedrill else os.getenv("OBSERVATION_TOPIC")
    pubstream = Stream(until_eos=True, auth=True)

    with pubstream.open(topic, "w") as ps:
        ps.write(message)
    click.secho(f"> Requesting heartbeat feedback via email for {detector_name}\n"
                f"> If the password is correct, the contact(s) for your experiment will receive an email.", fg='blue', bold=True)