""" CLI for snews_pt
    Right now publish method does not allow extra arguments.
    While this might be the desired use. I think it should not fail to publish, rather
    - either mark the extra columns and publish, or
    - split these columns, publish the fixed template, and report back to user.
    Manipulations in the publish class can be made see
    https://stackoverflow.com/questions/55099243/python3-dataclass-with-kwargsasterisk
"""

from . import __version__
from . import snews_pt_utils
from .snews_pub import Publisher
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
        if 'detector_name' in data:
            experiment = data['detector_name']
    else: data = {'detector_name':experiment}

    tiers_list, names_list = snews_pt_utils._check_cli_request(tiers)
    pub = Publisher(env_path=env)
    for tier, name in zip(tiers_list, names_list):
        click.secho(f'\nPublishing to {name}; ', bold=True, fg='blue')
        message = tier(**data).message()
        pub.send(message)


@main.command()
@click.argument('tier', nargs=1)
def hearbeat():
    pass

@main.command()
@click.argument('tier', nargs=1)
def retract():
    pass

@main.command()
@click.argument('tier', nargs=1)
def message_schema(tier):
    tier = snews_pt_utils.check_aliases(tier)
    tier_data_pairs = {'CoincidenceTier':snews_pt_utils.coincidence_tier_data(),
                       'SignificanceTier':snews_pt_utils.sig_tier_data(),
                       'TimingTier':snews_pt_utils.time_tier_data(),
                       'FalseOBS':snews_pt_utils.retraction_data(),
                       'Heartbeat':snews_pt_utils.heartbeat_data()}

    data = tier_data_pairs[tier]
    msg = msg_schema()
    all_data = msg.get_schema(tier, data, 'foo')
    click.secho(f'\t >The Message Schema for {tier}', bg='white', fg='blue')
    for k, v in all_data.items():
        if k not in data.keys():
            click.secho(f'{k:<20s}:(SNEWS SETS)', fg='red')
        else:
            click.secho(f'{k:<20s}:(User Input)', fg='blue')

if __name__ == "__main__":
    main()
