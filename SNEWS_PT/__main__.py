""" CLI for snews_pt
    Right now publish method does not allow extra arguments.
    While this might be the desired use. I think it should not fail to publish, rather
    - either mark the extra columns and publish, or
    - split these columns, publish the fixed template, and report back to user.
    Manipulations in the publish class can be made see
    https://stackoverflow.com/questions/55099243/python3-dataclass-with-kwargsasterisk
"""
#TODO: check the issue on Github and allow usage of combined message

from . import __version__
from . import snews_pt_utils
from .snews_pub import Publisher, Heartbeat, Retraction
from .snews_sub import Subscriber
from .message_schema import Message_Schema as msg_schema
import click
import os
import inspect


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

@main.command()
@click.argument('tiers', nargs=-1)
@click.option('--verbose','-v', type=bool, default=True)
@click.option('--file','-f', type=str, default="", show_default='data file')
@click.pass_context
def publish(ctx, tiers, file, verbose):
    """ Publish a message using snews_pub

    Notes
    -----
    The topics are read from the defaults i.e. from auxiliary/test-config.env
    If no file is given it can still submit dummy messages with default values
    """
    click.clear()
    tier_data_pairs = {'CoincidenceTier':snews_pt_utils.coincidence_tier_data(),
                       'SigTier':snews_pt_utils.sig_tier_data(),
                       'TimeTier':snews_pt_utils.time_tier_data(),
                       'FalseOBS':snews_pt_utils.retraction_data(),
                       'Heartbeat':snews_pt_utils.heartbeat_data()}

    tiers_list, names_list = snews_pt_utils._check_cli_request(tiers)
    for Tier, name in zip(tiers_list, names_list):
        click.secho(f'\nPublishing to {name}; ', bold=True, fg='bright_cyan')
        # look for the data
        if file != "":
            data = snews_pt_utils._parse_file(file)
        else:
            # get default data for tier
            data = tier_data_pairs[name]
        if 'detector_name' in data.keys():
            detector = data['detector_name']
        else:
            detector = ctx.obj['DETECTOR_NAME']
        data['detector_name'] = detector
        # message = Tier(**data).message()
        # check if the input matches the required fields
        valid_data = {}
        sig = inspect.signature(Tier).parameters
        for k, v in data.items():
            if k not in sig:
                click.echo(click.style(k, fg='bright_magenta') + f' not a valid key for {name}')
            else:
                valid_data[k] = v
        message = Tier.from_dict(valid_data).message()
        pub = ctx.with_resource(Publisher(ctx.obj['env'], verbose=verbose))
        pub.send(message)


@main.command()
@click.pass_context
def subscribe(ctx):
    """ Subscribe to Alert topic
    """
    sub = Subscriber(ctx.obj['env'])
    try:
        sub.subscribe()
    except KeyboardInterrupt:
        pass


@main.command()
@click.argument('status', nargs=1)
@click.option('--machine_time','-mt', type=str)
@click.option('--verbose','-v', type=bool, default=True)
@click.pass_context
def heartbeat(ctx, status, machine_time, verbose):
    click.secho(f'\nPublishing to Heartbeat; ', bold=True, fg='bright_cyan')
    message = Heartbeat(detector_name=ctx.obj['detector'], status=status, machine_time=machine_time).message()
    pub = ctx.with_resource(Publisher(ctx.obj['env'], verbose=verbose))
    pub.send(message)


@main.command()
@click.option('--tier','-t', nargs=1, help='Name of tier you want to retract from')
@click.option('--number','-n', type=int, default=1, help='Number of most recent message you want to retract')
@click.option('--reason','-r', type=str, default='', help='Retraction reason')
@click.option('--verbose','-v', type=bool, default=True)
@click.pass_context
def retract(ctx, tier, number, reason, verbose):
    click.secho(f'\nRetracting from {tier}; ', bold=True, fg='bright_magenta')
    message = Retraction(detector_name=ctx.obj['detector'],
                         which_tier=tier,
                         n_retract_latest=number,
                         retraction_reason=reason).message()
    pub = ctx.with_resource(Publisher(ctx.obj['env'], verbose=verbose))
    pub.send(message)

@main.command()
@click.argument('tier', nargs=1, default='all')
def message_schema(tier):
    """ Display the message format for `tier`, default 'all'

    Notes
    TODO: For some reason, the displayed keys are missing
    """
    tier_data_pairs = {'CoincidenceTier':snews_pt_utils.coincidence_tier_data(),
                       'SigTier':snews_pt_utils.sig_tier_data(),
                       'TimeTier':snews_pt_utils.time_tier_data(),
                       'FalseOBS':snews_pt_utils.retraction_data(),
                       'Heartbeat':snews_pt_utils.heartbeat_data()}

    if tier.lower()=='all':
        # display all formats
        tier = list(tier_data_pairs.keys())
    else:
        # check for aliases e.g. coinc = coincidence = CoinCideNceTier
        tier = snews_pt_utils._check_aliases(tier)

    # get message format for given tier(s)
    msg = msg_schema()
    for t in tier:
        data = tier_data_pairs[t]
        all_data = msg.get_schema(t, data, 'foo')
        click.secho(f'\t >The Message Schema for {t}', bg='white', fg='blue')
        for k, v in all_data.items():
            if k not in data.keys():
                click.secho(f'{k:<20s}:(SNEWS SETS)', fg='bright_red')
            else:
                click.secho(f'{k:<20s}:(User Input)', fg='bright_cyan')
        click.echo()

if __name__ == "__main__":
    main()
