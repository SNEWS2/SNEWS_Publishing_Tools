""" CLI for snews_pt
    
    Notes to dev team
    https://stackoverflow.com/questions/55099243/python3-dataclass-with-kwargsasterisk
"""
import time

from . import __version__
from . import snews_pt_utils
from .snews_pub import Publisher, SNEWSTiersPublisher
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
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
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
            SNEWSTiersPublisher.from_json(jsonfile=f, env_file=ctx.obj['env']).send_to_snews(firedrill)

        else:
            # maybe just print instead of raising
            raise TypeError(f"Expected json file with .json format! Got {f}")


@main.command()
@click.option('--plugin', '-p', type=str, default="None")
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.pass_context
def subscribe(ctx, plugin, firedrill):
    """ Subscribe to Alert topic
        Optionally, `plugin` script can be passed
        The message content as a single dictionary will be passed to 
        this script as a positional argument.
        dictionary follows the snews_alert message schema

    """
    sub = Subscriber(ctx.obj['env'], firedrill_mode=firedrill)
    try:
        if plugin != "None":
            print(f"Redirecting output to {plugin}")
            for saved_json in sub.subscribe_and_redirect_alert():
                os.system(f"python {plugin} {saved_json}")
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
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
def run_scenarios(firedrill):
    """
    """
    base = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base, 'auxiliary/try_scenarios.py')
    os.system(f'python3 {path} {firedrill}')


@main.command()
@click.option('--firedrill/--no-firedrill', default=True, show_default='True', help='Whether to use firedrill brokers or default ones')
@click.pass_context
def test_connection(ctx, firedrill):
    """ test the server connection
        It should prompt your whether the
        coincidence script is running in the server
    """
    from hop import Stream
    import time
    name = ctx.obj['DETECTOR_NAME']
    stamp_time = snews_pt_utils.TimeStuff().get_utcnow()
    message = {'_id': 'test-connection',
               'name': name,
               'time': stamp_time,
               'status': 'sending'}

    if firedrill:
        topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC")
    else:
        topic = os.getenv("OBSERVATION_TOPIC")
    substream = Stream(until_eos=False, auth=True, start_at=-5)
    pubstream = Stream(until_eos=True, auth=True)
    click.secho(f"> Testing your connection to {topic}. \nShould take 4-5 seconds...\n", fg='green')

    with substream.open(topic, "r") as ss, pubstream.open(topic, "w") as ps:
        ps.write(message)
        time_start = time.time()
        for read in ss:
            message_expected = message.copy()
            message_expected["status"] = "received"
            if read == message_expected:
                click.secho(f"You ({read['name']}) have a connection to the server at {read['time']}", fg='green', bold=True)
                break
            else:
                if time.time()-time_start > 3:
                    click.secho("I waited 3 second, couldn't find connection\n"
                                "Something is not right, try again!", fg='red')
                    break
                else:
                    continue


if __name__ == "__main__":
    main()
