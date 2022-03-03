""" CLI for snews_pt
    
    Notes to dev team
    https://stackoverflow.com/questions/55099243/python3-dataclass-with-kwargsasterisk
"""

from . import __version__
from . import snews_pt_utils
from .snews_pub import Publisher
from .snews_sub import Subscriber
from .snews_pt_utils import coincidence_tier_data, sig_tier_data, time_tier_data
from .snews_pt_utils import retraction_data, heartbeat_data
import click
import os
from inspect import signature

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
@click.option('--verbose','-v', type=bool, default=True)
@click.argument('file', nargs=-1)
@click.pass_context
def publish(ctx, file, verbose):
    """ Publish a message using snews_pub, multiple files are allowed
    Examples
    --------
    $: snews_pt publish my_json_message.json

    Notes
    -----
    The topics are read from the defaults i.e. from auxiliary/test-config.env
    If no file is given it can still submit dummy messages with default values
    """
    click.clear()
    for f in file:
        if f.endswith('.json'):
            data = snews_pt_utils._parse_file(f)
        else:
            raise TypeError(f"Expected json file with .json format! Got {f}")

        messages, names_list = snews_pt_utils._tier_decider(data)
        pub = ctx.with_resource(Publisher(ctx.obj['env'], verbose=verbose))
        pub.send(messages)


@main.command()
@click.option('--plugin', '-p', type=str, default="None")
@click.pass_context
def subscribe(ctx, plugin):
    """ Subscribe to Alert topic
        Optionally, `plugin` script can be passed
        The message content as a single dictionary will be passed to 
        this script as a positional argument.
        dictionary follows the snews_alert message schema

    """
    sub = Subscriber(ctx.obj['env'])
    try:
        if plugin != "None":     
            for alert_message in sub.subscribe_and_redirect_alert():   
                os.system(f"python {plugin} {alert_message}")
        else:
            sub.subscribe()             
    except KeyboardInterrupt:
        pass


@main.command()
@click.argument('requested_tier', nargs=-1)
@click.pass_context
def message_schema(ctx, requested_tier):
    """ Display the message format for `tier` if 'all'
        displays everything

    """
    detector = ctx.obj['DETECTOR_NAME']
    detector_str = click.style(detector, fg='yellow')
    tier_data_pairs = {'CoincidenceTier': (coincidence_tier_data, 'neutrino_time'),
                       'SigTier': (sig_tier_data, 'p_values'),
                       'TimeTier': (time_tier_data, 'timing_series'),
                       'FalseOBS': (retraction_data, 'n_retract_latest'),
                       'Heartbeat': (heartbeat_data, 'detector_status')}

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
            tier = snews_pt_utils._check_aliases(requested_tier[0])

    for t in tier:
        tier_keys = list(signature(tier_data_pairs[t][0]).parameters.keys())
        tier_keys.pop(tier_keys.index('meta'))
        must_key = tier_data_pairs[t][1]
        click.secho(f'\t >The Message Schema for {t}', bg='white', fg='blue')
        click.secho(f"{'_id':<20s}:(SNEWS SETS)", fg='bright_red')
        click.secho(f"{'schema_version':<20s}:(SNEWS SETS)", fg='bright_red')
        click.echo(click.style(f"{'detector_name':<20s}:(FETCHED FROM ENV {detector_str})", fg='red'))
        for key in tier_keys:
            if key == must_key:
                click.secho(f'{key:<20s}:(User Input*)', fg='bright_cyan')
            else:
                click.secho(f'{key:<20s}:(User Input)', fg='bright_cyan')
        click.secho(f"{'**kwargs':<20s}:(APPENDED AS 'META')\n", fg='red')
        

@main.command()
def run_scenarios():
    """
    """
    base = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base, 'auxiliary/test_scenarios.py')
    os.system(f'python3 {path}')

if __name__ == "__main__":
    main()
