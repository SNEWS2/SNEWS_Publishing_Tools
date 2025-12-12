import json
import os
import warnings

import click
from dotenv import load_dotenv
from snews import messages

from . import snews_pt_utils
from .auxiliary.try_scenarios import try_scenarios
from .messages import Publisher
from .snews_sub import Subscriber

envpath = os.path.join(os.path.dirname(__file__), "auxiliary/test-config.env")
load_dotenv(envpath)

if int(os.getenv("HAS_NAME_CHANGED")) == 0:
    warning_text = click.style(
        'You are using default detector name "TEST"\n'
        "Please change this by snews_pt.snews_pt_utils.set_name()",
        fg="red",
    )
    warnings.warn(warning_text, UserWarning)


@click.group(invoke_without_command=True,
             context_settings={'max_content_width': 120},
             epilog='See https://snews-publishing-tools.readthedocs.io/en/latest/ for more details')
@click.version_option()
@click.option(
    "--env",
    type=str,
    default="/auxiliary/test-config.env",
    show_default="auxiliary/test-config.env",
    help="environment file containing the configurations",
)
@click.pass_context
def main(ctx, env):
    """User interface for snews_pt tools"""
    base = os.path.dirname(os.path.realpath(__file__))
    env_path = base + env
    ctx.ensure_object(dict)
    snews_pt_utils.set_env(env_path)
    ctx.obj["env"] = env
    ctx.obj["DETECTOR_NAME"] = os.getenv("DETECTOR_NAME")
    ctx.obj["USER_PASS"] = os.getenv("ADMIN_PASS", "NO_AUTH")


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    show_default="False",
    help="Force json file to overwrite env variables",
)
@click.option(
    "--verbose",
    "-v",
    default=0,
    show_default="0",
    help="Verbosity level. 0: no output, 1: print simple feedback, 2: print message details.",
)
@click.argument("file", nargs=-1)
@click.pass_context
def publish(ctx, file, firedrill, force, verbose):
    """Publish a message using snews_pub, multiple files are allowed

    $: snews_pt publish my_json_message.json

    Notes

    The topics are read from the defaults i.e. from auxiliary/test-config.env
    If no file is given it can still submit dummy messages with default values
    """

    def _check_detector_name(json_detector_name, env_detector_name, force):
        """Check if detector name in json file matches the environment detector name.
        Defaults to env name. The json file name can be used with the --force flag
        """

        if force:
            click.secho(f"Forcing detector name from json file: "
                        f"{click.style(json_detector_name, bold=True)}")
            return json_detector_name

        if json_detector_name != env_detector_name:
            click.secho(
                f"{click.style('Warning:', bg='red')} "
                f"Detector name in JSON file ({click.style(json_detector_name, bold=True)}) "
                f"does not match the environment detector name "
                f"{click.style(env_detector_name, bold=True)}",
                fg="red", color="black"
            )
            click.secho(
                f"{click.style('Warning:', bg='red')} "
                f"Using environment detector name "
                f"{click.style(env_detector_name, bold=True)} "
                f"for this message. "
                f"To change the detector name, use the `snews_pt set-name` command.",
            )
        return env_detector_name

    if firedrill:
        publisher = Publisher(kafka_topic=os.getenv("FIREDRILL_OBSERVATION_TOPIC"))
    else:
        publisher = Publisher(kafka_topic=os.getenv("OBSERVATION_TOPIC"))

    env_detector_name = ctx.obj["DETECTOR_NAME"]
    for filename in file:
        if filename.endswith(".json"):
            try:
                with open(filename, "r", encoding="utf-8") as json_file:
                    json_data = json.load(
                        json_file
                    )
                    snews_messages = messages.create_messages(**json_data)
                    for message in snews_messages:
                        _detector_name = _check_detector_name(
                            message.detector_name, env_detector_name, force)
                        message.detector_name = _detector_name
                        publisher.add_message(message)
                    publisher.send(verbose=verbose)

            except FileNotFoundError:
                click.echo(f"Error: File not found: {filename}")
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON in {filename}: {e}")
            except Exception as e:
                click.echo(f"An unexpected error occurred: {e}")

        else:
            raise TypeError(f"Expected json file with .json format! Got {filename}")


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--status",
    "-s",
    type=str,
    default="OFF",
    show_default="OFF",
    help="Heartbeat at the time of execution",
)
@click.option(
    "--time",
    "-t",
    type=str,
    default=None,
    show_default="None",
    help="Machine time, format: %Y-%m-%dT%H:%M:%S.%f",
)
@click.option(
    "--verbose",
    "-v",
    default=0,
    show_default="0",
    help="Verbosity level. 0: no output, 1: print simple feedback, 2: print message details.",
)
@click.pass_context
def heartbeat(ctx, status, time, firedrill, verbose):
    """Publish heartbeat message

    :param status: Status of the experiment ON/OFF.
    :param time: (optional) Machine time is appended as the time of execution
                 different time can be passed following the iso-format
    """

    if firedrill:
        publisher = Publisher(kafka_topic=os.getenv("FIREDRILL_OBSERVATION_TOPIC"))
    else:
        publisher = Publisher(kafka_topic=os.getenv("OBSERVATION_TOPIC"))

    message = messages.HeartbeatMessage(
        detector_name=ctx.obj["DETECTOR_NAME"],
        machine_time_utc=time,
        detector_status=status,
        is_firedrill=firedrill,
    )

    publisher.add_message(message)
    publisher.send(verbose=verbose)


@main.command()
@click.option("--plugin", "-p", type=str, default="None")
@click.option("--outputfolder", "-o", type=str, default="None")
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--test/--no-test",
    default=False,
    show_default="False",
    help="If True subscribe to test topic",
)
@click.pass_context
def subscribe(ctx, plugin, outputfolder, firedrill, test):
    """Subscribe to Alert topic

    Optionally, `plugin` script can be passed
    The message content as a single dictionary will be passed to
    this script as a positional argument.
    dictionary follows the snews_alert message schema

    """
    sub = Subscriber(ctx.obj["env"], firedrill_mode=firedrill)
    try:
        if plugin != "None":
            print(f"Redirecting output to {plugin}")
            for saved_json in sub.subscribe_and_redirect_alert(
                outputfolder=outputfolder, is_test=test
            ):
                os.system(f"python {plugin} {saved_json}")
        else:
            sub.subscribe(outputfolder=outputfolder, is_test=test)
    except KeyboardInterrupt:
        pass


@main.command()
@click.argument("requested_tier", nargs=-1)
@click.pass_context
def message_schema(ctx, requested_tier):
    """Display the message format for each `tier`

    If 'all' is passed, displays everything.
    """

    valid_tiers = [
        m.replace("Message", "") for m in messages.__all__ if m.endswith("Message")
    ]

    if len(requested_tier) == 0:
        requested_tier = ["all"]

    get_all_tiers = requested_tier[0] == "all"  # it's a bool flag to print all tiers

    # Check for invalid tiers and echo if any requested tier is not valid
    if not get_all_tiers:
        invalid_tiers = [t for t in requested_tier if t not in valid_tiers]
        if invalid_tiers:
            click.echo(f"Warning: The following requested tiers are not valid: {', '.join(invalid_tiers)}")
            click.echo(f"Valid tiers are: {', '.join(valid_tiers)}")

    tiers = (
        valid_tiers
        if get_all_tiers  # if True, print all tiers
        else [t for t in requested_tier if t in valid_tiers]  # if False, print only the requested tiers
    )

    for t in tiers:
        tier_message = getattr(messages, t + "Message")
        fields = messages.get_fields(tier_message)
        reqfields = messages.get_fields(tier_message, required=True)

        click.secho(f"Message schema for {t}", bg="white", fg="blue")
        for f in fields:
            if f in reqfields:
                click.secho(f"{f:<20s} : (REQUIRED USER INPUT)", fg="bright_blue")
            else:
                click.secho(f"{f:<20s} : (USER INPUT)", fg="bright_cyan")
        click.secho(f'{"**kwargs":<20s} : (GROUPED AS META)\n', fg="bright_green")


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--test/--no-test",
    default=False,
    show_default="False",
    help="If True subscribe to test topic",
)
def run_scenarios(firedrill, test):
    """Test different coincidence scenarios"""
    # base = os.path.dirname(os.path.realpath(__file__))
    # path = os.path.join(base, 'auxiliary/try_scenarios.py')
    # os.system(f'python3 {path} {firedrill} {test}')
    try_scenarios(fd_mode=firedrill, is_test=test)


@main.command()
@click.option(
    "--name", "-n", default="TEST", show_default="TEST", help="Set the detectors name"
)
def set_name(name):
    """Set your detectors name"""
    from .snews_pt_utils import set_name as _set_name

    _set_name(name)
    click.secho(
        f"Your detector name is set to be: {os.environ['DETECTOR_NAME']}",
        fg="green",
        bold=True,
    )


# Remote Commands
@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--start_at", "-s", type=str, default="LATEST", help="either LATEST or EARLIEST"
)
@click.option("--patience", "-p", type=int, default=8)
@click.pass_context
def test_connection(ctx, firedrill, start_at, patience):
    """Test the connection to the server

    It should prompt your whether the coincidence script is running in the server
    :param start_at: `str` Where to start looking for the confirmation LATEST or EARLIEST
    :param patience: `int` seconds to wait before the check
        Sometime, it takes time for server to respond, increase patience
    """
    from .remote_commands import test_connection

    test_connection(
        detector_name=ctx.obj["DETECTOR_NAME"],
        firedrill=firedrill,
        start_at=start_at,
        patience=patience,
    )


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.pass_context
def write_hb_logs(ctx, firedrill):
    """REQUIRES AUTHORIZATION | Print the HB logs on the server standard output

    later admins can see them remotely
    """
    from .remote_commands import write_hb_logs

    write_hb_logs(
        detector_name=ctx.obj["DETECTOR_NAME"],
        admin_pass=ctx.obj["USER_PASS"],
        firedrill=firedrill,
    )


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option(
    "--test/--no-test",
    default=False,
    show_default="False",
    help="If True subscribe to test topic",
)
@click.pass_context
def reset_cache(ctx, firedrill, test):
    """REQUIRES AUTHORIZATION | Drop the current cache at the server
    """
    from .remote_commands import reset_cache

    reset_cache(
        detector_name=ctx.obj["DETECTOR_NAME"],
        admin_pass=ctx.obj["USER_PASS"],
        firedrill=firedrill,
        is_test=test,
    )


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.option("--brokername", "-bn", help="Change the broker")
@click.pass_context
def change_broker(ctx, firedrill, brokername):
    """REQUIRES AUTHORIZATION | If authorized, server changes the broker
    """
    from .remote_commands import change_broker

    change_broker(
        brokername=brokername,
        detector_name=ctx.obj["DETECTOR_NAME"],
        admin_pass=ctx.obj["USER_PASS"],
        firedrill=firedrill,
    )


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=True,
    show_default="True",
    help="Whether to use firedrill brokers or default ones",
)
@click.pass_context
def get_feedback(ctx, firedrill):
    """REQUIRES AUTHORIZATION | Get heartbeat feedback by email
    """
    from .remote_commands import get_feedback

    get_feedback(detector_name=ctx.obj["DETECTOR_NAME"], firedrill=firedrill)


if __name__ == "__main__":
    main()
