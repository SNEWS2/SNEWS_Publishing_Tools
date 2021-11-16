from . import __version__
from . import snews_pt_utils
from .message_schema import Message_Schema as msg_schema
import click
from datetime import datetime

@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.option('--env', type=str,
    default='./SNEWS_PT/auxiliary/test-config.env',
    show_default='auxiliary/test-config.env',
    help='environment file containing the configurations')
def main(env):
    """ User interface for snews_pt tools
    """
    snews_pt_utils.set_env(env)

@main.command()
@click.argument('tiers', nargs=-1)
@click.option('--experiment','-e', type=str, default="TEST", show_default='test experiment properties')
@click.option('--file','-f', type=str, default="", show_default='data file')
# @click.option('--bypass/--no-bypass', default=True, show_default='True', help='if False, asks user to modify the content of a message')
@click.option('--env', default=None, show_default='test-config.env', help='environment file containing the configurations')
def publish(tiers, experiment, file, env):
    """ Publish a message using snews_pub

    Notes
    -----
    If neither broker nor env filepath is given, first checks if the topic
    is set in the environment (i.e. os.getenv('X_TOPIC')). If not, sets
    this topic from the defaults i.e. from auxiliary/test-config.env
    If a different broker than that is set by the environment variables
    is passed. This overwrites the existing broker at the given topic.
    ::: if a different broker is given we can also make it the new env var
    """
    click.clear()
    if file != "":
        data = snews_pt_utils._parse_file(file)
        if 'detector' in data:
            experiment = data['detector']
    else: data = {'detector':experiment}
    pubs, names = snews_pt_utils._check_cli_request(tiers, experiment, env)
    for pub, name in zip(pubs, names):
        click.secho(f'\n > Publishing to {name}', fg='blue')
        pub(**data)


@main.command()
@click.argument('tier', nargs=1)
def message_schema(tier):
    tier = tier.lower()
    msg = msg_schema()
    if tier in ['coincidence', 'c', 'coincidencetier']:
        data = snews_pt_utils.coincidence_tier_data()
        tiername = 'CoincidenceTier'
        all_data = msg.get_schema(tiername,data, 'foo')
    elif tier in ['significance','s', 'significancetier']:
        data = snews_pt_utils.sig_tier_data()
        tiername = 'SignificanceTier'
        all_data = msg.get_schema(tiername, data, 'foo')
    elif tier in ['timing','t', 'timingtier']:
        data = snews_pt_utils.time_tier_data()
        tiername = 'TimingTier'
        all_data = msg.get_schema(tiername, data, 'foo')
    elif tier in ['heartbeat', 'hb']:
        data = snews_pt_utils.heartbeat_data()
        tiername = 'Heartbeat'
        all_data = msg.get_schema(tiername, data, 'foo')
    elif tier in ['falseobs', 'false']:
        data = snews_pt_utils.retraction_data()
        tiername = 'FalseOBS'
        all_data = msg.get_schema(tiername, data, 'foo')
    else:
        click.secho(f'{tier} is not valid! ')
        return None

    click.secho(f'\t >The Message Schema for {tiername}', bg='white', fg='blue')
    for k, v in all_data.items():
        if k not in data.keys():
            click.secho(f'{k:<20s}:(SNEWS SETS)', fg='red')
        else:
            click.secho(f'{k:<20s}:(User Input)', fg='blue')


if __name__ == "__main__":
    main()
