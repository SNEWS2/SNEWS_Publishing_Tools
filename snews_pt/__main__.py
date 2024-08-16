import os
import warnings

import click
from dotenv import load_dotenv
from . import snews_pt_utils
from ._version import version as __version__
from .snews_sub import Subscriber

envpath = os.path.join(os.path.dirname(__file__), 'auxiliary/test-config.env')
load_dotenv(envpath)

if int(os.getenv("HAS_NAME_CHANGED")) == 0:
    warning_text = click.style('You are using default detector name "TEST"\n'
                               'Please change this by snews_pt.snews_pt_utils.set_name()',
                               fg='red')
    warnings.warn(warning_text, UserWarning)


@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.option('--env', type=str,
    default='/auxiliary/test-config.env',
    show_default='auxiliary/test-config.env',
    help='environment file containing the configurations')
@click.pass_context
def main(ctx, env):
    """ User interface for snews_pt tools
    """
    base = os.path.dirname(os.path.realpath(__file__))
    env_path = base + env
    ctx.ensure_object(dict)
    snews_pt_utils.set_env(env_path)
    ctx.obj['env'] = env
    ctx.obj['DETECTOR_NAME'] = os.getenv("DETECTOR_NAME")
    ctx.obj['USER_PASS'] = os.getenv("ADMIN_PASS", "NO_AUTH")


@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True',
              help='Whether to use firedrill brokers or default ones')
@click.argument('file', nargs=-1)
@click.pass_context
def publish(ctx, file, firedrill):
    """ Publish a message using snews_pub, multiple files are allowed

    $: snews_pt publish my_json_message.json

    Notes

    The topics are read from the defaults i.e. from auxiliary/test-config.env
    If no file is given it can still submit dummy messages with default values
    """
    click.clear()
    for f in file:
        if f.endswith('.json'):
            SNEWSMessageBuilder.from_json(jsonfile=f, env_file=ctx.obj['env']).send_messages(firedrill_mode=firedrill)

        else:
            # maybe just print instead of raising
            raise TypeError(f"Expected json file with .json format! Got {f}")

@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--status', '-s', type=str, default='OFF', show_default='OFF', help='Heartbeat at the time of execution')
@click.option('--time', '-t', type=str, default=None, show_default='None', help='Machine time, format: %Y-%m-%dT%H:%M:%S.%f')
@click.pass_context
def heartbeat(ctx, status, time, firedrill):
    """ Send Heartbeats
        :param status: Status of the experiment ON/OFF.
        :param time: (optional) Machine time is appended as the time of execution
                     different time can be passed following the iso-format
    """
    message = SNEWSMessageBuilder(detector_name=ctx.obj['DETECTOR_NAME'],
                                  machine_time=time,
                                  detector_status=status,
    )
    message.send_messages(firedrill_mode=firedrill)


@main.command()
@click.option('--plugin', '-p', type=str, default="None")
@click.option('--outputfolder', '-o', type=str, default="None")
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--test/--no-test', default=False, show_default='False', help='If True subscribe to test topic')
@click.pass_context
def subscribe(ctx, plugin, outputfolder, firedrill, test):
    """ Subscribe to Alert topic
        Optionally, `plugin` script can be passed
        The message content as a single dictionary will be passed to
        this script as a positional argument.
        dictionary follows the snews_alert message schema

    """
    outputfolder = None if type(outputfolder)==type(None) else outputfolder
    sub = Subscriber(ctx.obj['env'], firedrill_mode=firedrill)
    try:
        if plugin != "None":
            print(f"Redirecting output to {plugin}")
            for saved_json in sub.subscribe_and_redirect_alert(outputfolder=outputfolder, is_test=test):
                os.system(f"python {plugin} {saved_json}")
        else:
            sub.subscribe(outputfolder=outputfolder, is_test=test)
    except KeyboardInterrupt:
        pass

@main.command()
@click.argument('requested_tier', nargs=-1)
@click.pass_context
def message_schema(ctx, requested_tier):
    """ Display the message format for `tier` if 'all'
        displays everything
    """
    from .messages import SNEWSHeartbeatMessage, SNEWSTimingTierMessage, SNEWSSignificanceTierMessage, \
        SNEWSCoincidenceTierMessage, SNEWSRetractionMessage, SNEWSMessage

    tier_data_pairs = {'CoincidenceTier': SNEWSCoincidenceTierMessage,
                       'SigTier': SNEWSSignificanceTierMessage,
                       'TimeTier': SNEWSTimingTierMessage,
                       'FalseOBS': SNEWSRetractionMessage,
                       'Heartbeat': SNEWSHeartbeatMessage,}

    if len(requested_tier)>1:
        tier = []
        for t in requested_tier:
            tier.append(snews_pt_utils._check_aliases(t))
    else:
        if requested_tier[0].lower()=='all':
            # display all
            tier = list(tier_data_pairs.keys())
        else:
            # check for aliases e.g. coinc = coincidence = CoinCideNceTier
            tier = list(snews_pt_utils._check_aliases(requested_tier[0]))

    basefields = SNEWSMessage.basefields
    for t in tier:
        TierMessage = tier_data_pairs[t]
        fields = TierMessage.fields
        reqfields = TierMessage.reqfields
        click.secho(f'Message schema for {t}', bg='white', fg='blue')
        for f in fields:
            if f in basefields:
                click.secho(f'{f:<20s} : (SET AUTOMATICALLY)', fg='bright_red')
            elif f in reqfields:
                click.secho(f'{f:<20s} : (REQUIRED USER INPUT)', fg='bright_blue')
            else:
                click.secho(f'{f:<20s} : (USER INPUT)', fg='bright_cyan')
        click.secho(f'{"**kwargs":<20s} : (GROUPED AS META)', fg='bright_green')

@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--test/--no-test', default=True, show_default='True', help='If False sends them to main topic!')
def run_scenarios(firedrill, test):
    """
    """
    base = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base, 'auxiliary/try_scenarios.py')
    os.system(f'python3 {path} {firedrill} {test}')

@main.command()
@click.option('--name', '-n', default="TEST", show_default='TEST', help='Set the detectors name')
def set_name(name):
    """ Set your detectors name
    """
    from .snews_pt_utils import set_name as _set_name
    _set_name(name)
    click.secho(f"Your detector name is set to be: {os.environ['DETECTOR_NAME']}", fg='green', bold=True)

###################### Remote Commands
@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--start_at', '-s', type=str, default="LATEST", help='either LATEST or EARLIEST')
@click.option('--patience', '-p', type=int, default=8)
@click.pass_context
def test_connection(ctx, firedrill, start_at, patience):
    """ test the server connection
        It should prompt your whether the coincidence script is running in the server
        :param start_at: `str` Where to start looking for the confirmation LATEST or EARLIEST
        :param patience: `int` seconds to wait before the check
            Sometime, it takes time for server to respond, increase patience
    """
    from .remote_commands import test_connection
    test_connection(detector_name=ctx.obj['DETECTOR_NAME'],
                    firedrill=firedrill, start_at=start_at, patience=patience)


@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.pass_context
def write_hb_logs(ctx, firedrill):
    """ REQUIRES AUTHORIZATION
        ask to print the HB logs on the server standard output
        later admins can see them remotely
    """
    from .remote_commands import write_hb_logs
    write_hb_logs(detector_name=ctx.obj['DETECTOR_NAME'],
                  admin_pass=ctx.obj['USER_PASS'],
                  firedrill=firedrill)

@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--test/--no-test', default=True, show_default='True', help='If True cleans the test cache')
@click.pass_context
def reset_cache(ctx, firedrill, test):
    """ REQUIRES AUTHORIZATION
        If authorized, drop the current cache at the server
    """
    from .remote_commands import reset_cache
    reset_cache(detector_name=ctx.obj['DETECTOR_NAME'],
                admin_pass=ctx.obj['USER_PASS'],
                firedrill=firedrill,
                is_test=test)


@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.option('--brokername', '-bn', help='Change the broker')
@click.pass_context
def change_broker(ctx, firedrill, brokername):
    """ REQUIRES AUTHORIZATION
        If authorized, server changes the broker
    """
    from .remote_commands import change_broker
    change_broker(brokername=brokername,
                  detector_name=ctx.obj['DETECTOR_NAME'],
                  admin_pass=ctx.obj['USER_PASS'],
                  firedrill=firedrill)


@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.pass_context
def get_feedback(ctx, firedrill):
    """ REQUIRES AUTHORIZATION
        Get heartbeat feedback by email
    """
    from .remote_commands import get_feedback
    get_feedback(detector_name=ctx.obj['DETECTOR_NAME'],
                 firedrill=firedrill)

if __name__ == "__main__":
    main()
