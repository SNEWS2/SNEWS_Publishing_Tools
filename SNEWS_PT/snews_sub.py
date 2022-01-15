
import os, json, click
from hop import Stream
from . import snews_pt_utils


def save_message(message):
    """ Save messages to a json file.

    """
    S = Subscriber()
    path = f'SNEWS_MSGs/{S.times.get_date()}/'
    os.makedirs(path, exist_ok=True)
    file = path + 'subscribed_messages.json'
    # read the existing file
    try:
        data = json.load(open(file))
        if not isinstance(data, dict):
            print('Incompatible file format!')
            return None
        # TODO: deal with `list` type objects
    except:
        data = {}
    # add new message with a current time stamp
    current_time = S.snews_time()
    data[current_time] = message
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

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
#             _v = []                        # tmp fix, it crashes if there were None's in the list
#             for item in v:
#                 if type(item)==type(None):
#                     _v.append('None')
#                 else:
#                     _v.append(item)
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

    """
    def __init__(self, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.alert_topic = os.getenv("ALERT_TOPIC")
        self.times = snews_pt_utils.TimeStuff()

        # time object/strings
        self.times = snews_pt_utils.TimeStuff(env_path)
        self.hr = self.times.get_hour()
        self.date = self.times.get_date()
        self.snews_time = lambda: self.times.get_snews_time()


    def subscribe(self):
        ''' Subscribe and listen to a given topic

        Parameters
        ----------
            Whether to display the subscribed message content

        '''
        click.echo('You are subscribing to ' +
                   click.style(f'ALERT', bg='red', bold=True) + '\nBroker:' +
                   click.style(f'{ self.alert_topic}', bg='green'))

        # Initiate hop_stream
        stream = Stream(until_eos=False)
        try:
            with stream.open(self.alert_topic, "r") as s:
                for message in s:
                    save_message(message)
                    snews_pt_utils.display_gif()
                    display(message)
        except KeyboardInterrupt:
            click.secho('Done', fg='green')
