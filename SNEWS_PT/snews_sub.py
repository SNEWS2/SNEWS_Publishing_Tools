
import os, json, click
from hop import Stream
from . import snews_pt_utils

def make_file(outputfolder):
    """ Get a proper json file name at a given folder
    """
    os.makedirs(outputfolder, exist_ok=True)
    date = snews_pt_utils.TimeStuff().get_date()
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
        json.dump(message, outfile, indent=4, sort_keys=True)
    if return_file:
        return file

def display(message):
    """ Function to format output messages
    """
    click.echo(click.style('ALERT MESSAGE'.center(65, '_'), bg='red', bold=True))
    for k, v in message.items():
        if type(v) == type(None): v = 'None'
        if type(v) == int:
            click.echo(f'{k:<20s}:{v:<45}')
        if type(v) == str:
            click.echo(f'{k:<20s}:{v:<45}')
        elif type(v) == list:
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
    firedrill_mode : bool
        tell Subscriber to get messages from the firedrill hop broker, defaults to False

    """
    def __init__(self, env_path=None, firedrill_mode=True):
        snews_pt_utils.set_env(env_path)
        self.alert_topic = os.getenv("ALERT_TOPIC")
        if firedrill_mode:
            self.alert_topic = os.getenv("FIREDRILL_ALERT_TOPIC")
        self.times = snews_pt_utils.TimeStuff()
        # time object/strings
        self.times = snews_pt_utils.TimeStuff(env_path)
        self.hr = self.times.get_hour()
        self.date = self.times.get_date()
        self.snews_time = lambda: self.times.get_utcnow()
        self.default_output = os.path.join(os.getcwd(), os.getenv("ALERT_OUTPUT"))


    def subscribe(self, outputfolder=None):
        """ Subscribe and listen to a given topic

        Parameters
        ----------
        outputfolder: `str`
            where to save the alert messages, if None
            creates a file based on env file

        """
        outputfolder = outputfolder or self.default_output
        # base = os.path.dirname(os.path.realpath(__file__))
        # outputfolder = os.path.join(base, outputfolder)
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    save_message(message, outputfolder)
                    snews_pt_utils.display_gif()
                    display(message)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')


    def subscribe_and_redirect_alert(self, outputfolder=None):
        """ subscribe generator
        """
        outputfolder = outputfolder or self.default_output
        # base = os.path.dirname(os.path.realpath(__file__))
        # outputfolder = os.path.join(base, outputfolder)
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    file = save_message(message, outputfolder, return_file=True)
                    snews_pt_utils.display_gif()
                    display(message)
                    # jsonformat = json.dumps(message)
                    yield file #make_file(outputfolder)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')
