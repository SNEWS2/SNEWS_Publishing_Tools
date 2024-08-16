
from datetime import datetime
import os, json, click
from hop import Stream
from . import snews_pt_utils

def make_file(outputfolder):
    """ Get a proper json file name at a given folder
        It applies an increment to the file name at a given folder to avoid overwrite

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
        Parameters
        ----------
        message : dict
            The incoming alert message
        outputfolder : str
            The path where to save the incoming alerts
        return_file : bool
            Whether to return file name as a string

    """
    file = make_file(outputfolder)
    with open(file, 'w') as outfile:
        json.dump(message, outfile, indent=4, sort_keys=True)

    if return_file:
        return file

def display(message):
    """ Display the incoming alert message on screen

    """
    click.echo(click.style('ALERT MESSAGE'.center(65, '_'), bg='red', bold=True))

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
    env_path : str
        path for the environment file. Use default settings if not given
    firedrill_mode : bool
        tell Subscriber to get messages from the firedrill hop broker, defaults to False

    """
    def __init__(self, env_path=None, firedrill_mode=True):
        snews_pt_utils.set_env(env_path)
        self.alert_topic = os.getenv("ALERT_TOPIC")
        self.connection_test_topic = os.getenv("CONNECTION_TEST_TOPIC")
        if firedrill_mode:
            self.alert_topic = os.getenv("FIREDRILL_ALERT_TOPIC")

        self.snews_time = datetime.utcnow().isoformat()
        self.default_output = os.path.join(os.getcwd(), os.getenv("ALERT_OUTPUT"))


    def subscribe(self, outputfolder=None, auth=True, is_test=False):
        """ Subscribe and listen to a given topic

        Parameters
        ----------
        outputfolder: str
            where to save the alert messages, if None, creates a file based on env file
        auth: A `bool` or :class:`Auth <hop.auth.Auth>` instance. Defaults to
            loading from :meth:`auth.load_auth <hop.auth.load_auth>` if set to
            True. To disable authentication, set to False.
        is_test: bool if True overwrites the subscribed topic with CONNECTION_TEST_TOPIC

        """
        outputfolder = outputfolder or self.default_output
        TOPIC = self.connection_test_topic if is_test else self.alert_topic

        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ TOPIC}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False, auth=auth)

        try:
            with stream.open(TOPIC, "r") as s:
                for message in s:
                    # Access message dictionary from JSOBlob
                    message = message.content
                    try:
                        if message['_id'] == "0_test-connection":
                            continue
                    except:
                        pass
                    # Save and display
                    save_message(message, outputfolder)
                    snews_pt_utils.display_gif()
                    display(message)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')


    def subscribe_and_redirect_alert(self, outputfolder=None, auth=True, _display=True, _return='file', is_test=False):
        """ subscribe generator
        """
        outputfolder = outputfolder or self.default_output
        TOPIC = self.connection_test_topic if is_test else self.alert_topic
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ TOPIC}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False, auth=auth)
        try:
            with stream.open(TOPIC, "r") as s:
                for message in s:
                    # Access message dictionary from JSONBlobg
                    message = message.content
                    try:
                        if message['_id'] == "0_test-connection":
                            continue
                    except:
                        pass
                    # Save and display
                    file = save_message(message, outputfolder, return_file=True)
                    if _display:
                        snews_pt_utils.display_gif()
                        display(message)
                    if _return == 'message':
                        yield message
                    else:
                        yield file
        except KeyboardInterrupt:
            click.secho('Done', fg='green')
