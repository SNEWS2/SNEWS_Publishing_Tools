"""
An interface for SNEWS member experiment 
to publish their observation and heartbeat messages.

Created: 
August 2021
Authors: 
Melih Kara
Sebastian Torres-Lara
Joe Smolsky
"""
from datetime import datetime
try:
    fromisoformat = datetime.fromisoformat
except AttributeError:
    from dateutil.parser import isoparse as fromisoformat
import os, click
from hop import Stream
try:
    from hop.models import JSONBlob
except ImportError:
    raise ImportError(f"SNEWS Publishing Tools and Coincidence System requires hop version>=0.8.0\n"
                      f"Please upgrade your `pip install -U hop-client`")
from . import snews_pt_utils
from .snews_format_checker import SnewsFormat
from .snews_pt_utils import prettyprint_dictionary
from .tier_decider import TierDecider

def homogenise_time_field(message):
    """ Make sure all messages follow the same ISO format.

    """
    # convert to iso-formatted datetime object and revert
    dateobj = fromisoformat(message["neutrino_time"])
    datestr = dateobj.isoformat()
    message["neutrino_time"] = datestr
    return message

def check_format(messages):
    """ Check if the messages are valid SnewsFormat
        Parameters
        ----------
        messages : dict
            The generated messages

        Returns
        -------
        valid, invalid : dict
            The valid/invalid messages

    """
    valid = []
    invalid = []
    for message in messages:
        if SnewsFormat(message)():
            if "neutrino_time" in message.keys():
                # homogenise the valid messages
                valid.append(homogenise_time_field(message))
            else:
                valid.append(message)
        else:
            invalid.append(message)
            click.secho(f'{"-" * 64}', fg='bright_red')
            click.secho(f'Skipping message! Improper format! see <self.invalid_messages>')
    return valid, invalid

class Publisher:

    def __init__(self, env_path=None, verbose=True, auth=True, firedrill_mode=True):
        """Class in charge of publishing messages to SNEWS-hop sever.
        This class acts as a context manager.

        Parameters
        ----------
        env_path: str
            path to SNEWS env file, defaults to tes_config.env if None is passed.
        verbose: bool
            Option to display message when publishing.
        auth: bool
            Option to run hop-Stream without authentication. Pass False to do so
        firedrill_mode :bool
            whether to use firedrill broker

        """
        snews_pt_utils.set_env(env_path)
        self.auth = auth
        self.verbose = verbose

        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        if firedrill_mode:
            self.obs_broker = os.getenv("FIREDRILL_OBSERVATION_TOPIC")


    def __enter__(self):
        self.stream = Stream(until_eos=True, auth=self.auth).open(self.obs_broker, 'w')
        return self

    def __exit__(self, *args):
        self.stream.close()

    def send(self, messages):
        """ This method will set the sent_time and send the message to the hop broker.

        Parameters
        ----------
        messages: `list`
            list containing observation message.

        """
        if len(messages) == 0:
            # None of the messages passed the format checker!
            raise UserWarning("No valid message exists!")

        if type(messages) == dict:
            messages = list(messages)
        for message in messages:
            message["sent_time"] = datetime.utcnow().isoformat()
            self.stream.write(JSONBlob(message))
            self.display_message(message)

            
    def display_message(self, message):
        if self.verbose:
            tier = message['_id'].split('_')[1]
            click.secho(f'{"-" * 64}', fg='bright_blue')
            click.secho(f'Sending message to {tier} on {self.obs_broker}', fg='bright_red')
            if tier == 'Retraction':
                click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
            prettyprint_dictionary(message)


class SNEWSTiersPublisher:

    def __init__(self, env_file=None,
                 detector_name='TEST',
                 machine_time=None,
                 neutrino_time=None,
                 p_val=None,
                 p_values=None,
                 t_bin_width=None,
                 timing_series=None,
                 retract_latest=None,
                 retraction_reason=None,
                 detector_status=None,
                 is_pre_sn=False,
                 firedrill_mode=True,
                 is_test=False,
                 **kwargs):
        """ SNEWS Publisher Instance, it lets you create message data and interact with them
        before publishing to snews. Submitting JSON files is also possible see
        SNEWSTierPublisher.from_json()

        Parameters
        ----------
        env_file: str
            path to env file, when None, uses the default env file
        detector_name: str
            Name of your detector,defaults to None.
            See auxiliary/detector_properties.json for available detector names.
        machine_time: str
            time recorded by your detector, defaults to None
            format: '%y/%m/%d %H:%M:%S:%f'
        neutrino_time: str
            time stamp of initial neutrino signal, defaults to None
            format: '%y/%m/%d %H:%M:%S:%f'
        p_val: float
            p value of possible observation, defaults to None
        p_values: `list`
            p values of individual neutrino observations, defaults to None.
            If passed, `t_bin_width` is also expected.
        t_bin_width: float
            width of time window [sec], required for significance tier, defaults to None.
            If passed, `p_values` is also expected.
        timing_series: list
            list of strings with individual neutrino times following ISO format defaults to None
        retract_latest: int
            how many of your last messages do you want to retract, defaults to None
        retraction_reason: str
            (optional) share with SNEWS what caused your false observation, defaults to None.
            We won't judge you :)
        detector_status: str
            Send "ON" or "OFF" heartbeats.
        is_pre_sn: bool
            Whether the message is triggered by pre-supernova neutrinos.
        firedrill_mode : bool
            tell Publisher to send messages to the firedrill hop broker, defaults to True
        is_test : bool
            True if the messages are meant for testing, then the time checks are ignored
        kwargs:
            Any additional key-word argument you want to send to SNEWS
        """
        if detector_name == "TEST":
            detector_name = snews_pt_utils.get_name()
        self.message_data = {'detector_name': detector_name,
                             'machine_time': machine_time,
                             'neutrino_time': neutrino_time,
                             'p_val': p_val,
                             'p_values': p_values,
                             't_bin_width': t_bin_width,
                             'timing_series': timing_series,
                             'retract_latest': retract_latest,
                             'retraction_reason': retraction_reason,
                             'detector_status': detector_status,
                             'is_pre_sn': is_pre_sn,
                             'is_test':is_test}
        self.meta = dict(**kwargs)
        self.message_data = {**self.message_data, ** self.meta}
        self.env_file = env_file
        self.firedrill_mode = firedrill_mode
        # split messages for different tiers, and format properly
        self.messages, self.tiernames = TierDecider(self.message_data).decide()
        # check the message contents
        self.messages, self.invalid_messages = check_format(self.messages)

    @classmethod
    def from_json(cls, jsonfile, env_file=None, **kwargs):
        """ Read the data from a json file
            Additional data / overwrite is allowed, by passing the key-value pair as additional arguments

            Parameters
            ----------
            jsonfile : str
                Path to your local JSON file
            env_file : str
                Path to your local environment file. If none, uses the default.
            **kwargs : key-value pairs
                Any other key-value pairs you want to pass or overwrite the ones in your JSON file

            Examples
            --------
            > read the data from "myheartbeat.json" and overwrite the detector_name
            publisher = SNEWSTierPublisher.from_json("myheartbeat.json", detector_name="IceCube")
            print(publisher.messages)
            publisher.send_to_snews()

        """
        input_json = snews_pt_utils._parse_file(jsonfile)
        output_data = {**input_json, **kwargs}
        return cls(env_file=env_file, **output_data)

    def send_to_snews(self, auth=True, verbose=True):
        """ Send the message to SNEWS

            Parameters
            ----------
            verbose : bool
                Whether to display the message sent
            auth : bool
                whether to authenticate with hop

        """
        with Publisher(env_path=self.env_file, verbose=verbose, auth=auth, firedrill_mode=self.firedrill_mode) as pub:
            pub.send(self.messages)
