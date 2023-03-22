
from datetime import datetime
import os, json, click
from hop import Stream
try:
    from hop.models import JSONBlob
    hop8 = True
except ImportError:
    hop8 = False
from . import snews_pt_utils

def make_file(outputfolder):
    """ Get a proper json file name at a given folder
    """
    os.makedirs(outputfolder, exist_ok=True)
    date = datetime.utcnow().isoformat().split('T')[0]
    file = os.path.join(outputfolder, f"0-SNEWS_ALERT_{date}.json")
    while os.path.isfile(file):
        i = int(file.split('/')[-1].split('-')[0])
        file = os.path.join(outputfolder, f"{i+1}-SNEWS_ALERT_{date}.json")
    return file

def save_message(message, outputfolder, return_file=False):
    """ Save messages to a json file.

    """
    file = make_file(outputfolder)
    with open(file, 'w') as outfile:
        
        if hop8:
            message = message.content

        json.dump(message, outfile, indent=4, sort_keys=True)

    if return_file:
        return file

def display(message):
    """ Function to format output messages
    """
    click.echo(click.style('ALERT MESSAGE'.center(65, '_'), bg='red', bold=True))

    if hop8:
        message = message.content

    for k, v in message.items():
        key_type = type(v)
        if key_type == type(None):
            v = 'None'

        if key_type in [int, float, str]:
            if k=='alert_type':
                if v=='RETRACTION':
                    click.echo(f'{k:<20s}' + click.style(f':{v:<45}', bg='red'))
                elif v=='UPDATE':
                    click.echo(f'{k:<20s}' + click.style(f':{v:<45}', bg='blue'))
                else:
                    click.echo(f'{k:<20s}:{v:<45}')
            else:
                click.echo(f'{k:<20s}:{v:<45}')

        elif key_type == list:
            v = [str(item) for item in v]
            items = '\t'.join(v)
            if k == 'detector_names':
                click.echo(f'{k:<20s}' + click.style(f':{items:<45}', bg='blue'))
            else:
                click.echo(f'{k:<20s}:{items:<45}')

    click.secho('_'.center(65, '_'), bg='bright_red')


class Subscriber:
    """ Class to subscribe ALERT message stream

    Parameters
    ----------
    env_path : `str`
        path for the environment file.
        Use default settings if not given
    firedrill_mode : `bool`
        tell Subscriber to get messages from the firedrill hop broker, defaults to False

    """
    def __init__(self, env_path=None, firedrill_mode=True):
        snews_pt_utils.set_env(env_path)
        self.alert_topic = os.getenv("ALERT_TOPIC")
        if firedrill_mode:
            self.alert_topic = os.getenv("FIREDRILL_ALERT_TOPIC")

        self.snews_time = datetime.utcnow().isoformat()
        self.default_output = os.path.join(os.getcwd(), os.getenv("ALERT_OUTPUT"))


    def subscribe(self, outputfolder=None, auth=True):
        """ Subscribe and listen to a given topic

        Parameters
        ----------
        outputfolder: `str`
            where to save the alert messages, if None
            creates a file based on env file
        auth: A `bool` or :class:`Auth <hop.auth.Auth>` instance. Defaults to
            loading from :meth:`auth.load_auth <hop.auth.load_auth>` if set to
            True. To disable authentication, set to False.

        """
        outputfolder = outputfolder or self.default_output
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False, auth=auth)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    save_message(message, outputfolder)
                    snews_pt_utils.display_gif()
                    display(message)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')


    def subscribe_and_redirect_alert(self, outputfolder=None,  auth=True):
        """ subscribe generator
        """
        outputfolder = outputfolder or self.default_output
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False, auth=auth)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    file = save_message(message, outputfolder, return_file=True)
                    snews_pt_utils.display_gif()
                    display(message)
                    yield file
        except KeyboardInterrupt:
            click.secho('Done', fg='green')
