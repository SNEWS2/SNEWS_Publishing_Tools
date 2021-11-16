"""
Example initial dosctring
"""
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple
import os, json, click
# from pathlib import Path
# import sys


def set_env(env_path=None):
    """ Set environment parameters

    Parameters
    ----------
    env_path : `str`, (optional)
        path for the environment file.
        Use default settings if not given

    """
    dirname = os.path.dirname(__file__)
    default_env_path = dirname + '/auxiliary/test-config.env'
    env = env_path or default_env_path
    load_dotenv(env)


class TimeStuff:
    ''' SNEWS format datetime objects

    '''

    def __init__(self, env_path=None):
        set_env(env_path)
        self.snews_t_format = os.getenv("TIME_STRING_FORMAT")
        self.hour_fmt = "%H:%M:%S"
        self.date_fmt = "%y_%m_%d"
        self.get_datetime = datetime.utcnow()
        self.get_snews_time = lambda fmt=self.snews_t_format: datetime.utcnow().strftime(fmt)
        self.get_hour = lambda fmt=self.hour_fmt: datetime.utcnow().strftime(fmt)
        self.get_date = lambda fmt=self.date_fmt: datetime.utcnow().strftime(fmt)

    def str_to_datetime(self, nu_time, fmt='%y/%m/%d %H:%M:%S'):
        """ string to datetime object """
        return datetime.strptime(nu_time, fmt)

    def str_to_hr(self, nu_time, fmt='%H:%M:%S:%f'):
        """ string to datetime hour object """
        return datetime.strptime(nu_time, fmt)


def set_topic_state(which_topic, env_path=None):
    """ Set the topic path based on which_topic

    Parameters
    ----------
    which_topic : `str`
        single-letter string indicating the topic [O/H/A]
        If an environment was defined, it uses the topics
        specified in that environment. If not, it looks
        for the env_path parameter
    env_path : `str`
        The path to the environment configuration file

    """
    if os.getenv("ALERT_TOPIC") == None: set_env(env_path)
    Topics = namedtuple('Topics', ['topic_name', 'topic_broker'])
    topics = {
        'A': Topics('ALERT', os.getenv("ALERT_TOPIC")),
        'O': Topics('OBSERVATION', os.getenv("OBSERVATION_TOPIC")),
        'H': Topics('HEARTBEAT', os.getenv("OBSERVATION_TOPIC"))
    }
    return topics[which_topic.upper()]


def retrieve_detectors(detectors_path=os.path.dirname(__file__) + "/auxiliary/detector_properties.json"):
    ''' Retrieve the name-ID-location of the participating detectors.

        Parameters
        ----------
        detectors_path : `str`, optional
            path to detector proporties. File needs to be
            in JSON format
        
        Returns
        -------
        None

    '''
    if not os.path.isfile(detectors_path):
        os.system(f'python {os.path.dirname(__file__)}/auxiliary/make_detector_file.py')

    with open(detectors_path) as json_file:
        detectors = json.load(json_file)

    # make a namedtuple
    Detector = namedtuple("Detector", ["name", "id", "location"])
    for k, v in detectors.items():
        detectors[k] = Detector(v[0], v[1], v[2])
    return detectors


def get_detector(detector, detectors_path=os.path.dirname(__file__) +
                                          "/auxiliary/detector_properties.json"):
    """ Return the selected detector properties

    Parameters
    ----------
    detector : `str`
        The name of the detector. Should be one of the predetermined detectors.
        If the name is not in that list, returns TEST detector.

    """
    Detector = namedtuple("Detector", ["name", "id", "location"])
    if isinstance(detector, Detector): return detector  # not needed?
    # search for the detector name in `detectors`
    detectors = retrieve_detectors(detectors_path)
    if isinstance(detector, str):
        try:
            return detectors[detector]
        except KeyError:
            print(f'{detector} is not a valid detector!')
            return detectors['TEST']


def summarize(detector, topic_type_, env_path=None):
    """ Summarize the current configuration (DEPRECATED)

    Parameters
    ----------
    detector : `str`
        name of the detector
    topic_type : `str`
        The topic that is subscribed

    Returns
    -------

    .. note:: Deprecated

    """
    import hop, snews, sys
    set_env()
    broker = os.getenv("HOP_BROKER")
    observation_topic = os.getenv("OBSERVATION_TOPIC")
    heartbeat_topic = os.getenv("OBSERVATION_TOPIC")
    alert_topic = os.getenv("ALERT_TOPIC")
    topic_type = f"Publish SNEWS {topic_type_} Messages"
    print(
        '#'.center(50, '#') +
        f'\n# {topic_type:^46} #\n'
        f'#{detector.name:_^48}#\n'
        f'#{str(detector.id) + "-" + detector.location:_^48}#\n' +
        '#'.center(50, '#') +
        f'\nYour Python version:\n {sys.version}\n'
        f'Current hop-client version:{hop.__version__}\n'
        f'             snews version:{snews.__version__}\n\n'
        f'Publishing to {broker}\n'
        f'Observation Topic:\n==> {observation_topic}\n'
        f'Heartbeat Topic:\n==> {heartbeat_topic}\n\n')


def data_obs(machine_time=None, nu_time=None, p_value=None, timing_series=None,
             detector_status=None, false_mgs_id=None, which_tier=None,
             N_retract_latest=0, retraction_reason=None, **kwargs):
    """ Default observation message data
        
        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        nu_time : `datetime`
            The neutrino arrival time
        p_value : `float`
            If determined, the p value of the observation
        timing_series : `array-like`
            Time series of the detected signal
        false_mgs_id : `str`
            The id of the message that is falsely published
        which_tier : 'str'
            OBS type of false message ['CoincidenceTier', 'SigTier', 'TimeTier, 'ALL']
        N_retract_latest: 'int' or 'str'
            Tells retraction methods to look for N  latest message sent by a detector. can also pass 'ALL'
            to retract all messages in a OBS tier.
        retraction_reason: 'str"
            Reason for message(s) retraction
        **kwargs 
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            data_dict : `dict`
                dictionary of the complete observation data

    """
    keys = ['machine_time', 'neutrino_time', 'p_value', 'timing_series', 'false_id',
            'N_retract_latest', 'which_tier', 'retraction_reason']
    values = [machine_time, nu_time, p_value, timing_series, false_mgs_id, N_retract_latest,
              which_tier, retraction_reason]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    data_dict = dict(zip_iterator)
    return data_dict


def coincidence_tier_data(machine_time=None, nu_time=None, p_value=None, **kwargs):
    """ Formats data for CoincidenceTier as dict object

        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        nu_time : `datetime`
            The neutrino arrival time
        p_value : `float`
            If determined, the p value of the observation
        **kwargs
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            coincidence_tier_dict : `dict`
                dictionary of the complete CoincidenceTier data

    """
    keys = ['machine_time', 'neutrino_time', 'p_value']
    values = [machine_time, nu_time, p_value]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    coincidence_tier_dict = dict(zip_iterator)
    return coincidence_tier_dict


def sig_tier_data(machine_time=None, nu_time=None, p_values=None, **kwargs):
    """ Formats data for SigTier as dict object

        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        nu_time : `datetime`
            The neutrino arrival time
        p_values : `arr`
            If determined, the p value of the observation
        **kwargs
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            sig_tier_dict : `dict`
                dictionary of the complete observation data

    """
    keys = ['machine_time', 'neutrino_time', 'p_values']
    values = [machine_time, nu_time, p_values]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    sig_tier_dict = dict(zip_iterator)
    return sig_tier_dict


def time_tier_data(machine_time=None, nu_time=None, timing_series=None,
                  **kwargs):
    """ Formats data for TimingTier as dict object

        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        nu_time : `datetime`
            The neutrino arrival time
        timing_series : `array-like`
            Time series of the detected signal
        **kwargs
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            data_dict : `dict`
                dictionary of the TimingTier data

    """
    keys = ['machine_time', 'neutrino_time', 'timing_series']
    values = [machine_time, nu_time, timing_series]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    time_tier_dict = dict(zip_iterator)
    return time_tier_dict


def retraction_data(machine_time=None, false_mgs_id=None, which_tier=None,
                        n_retract_latest=0, retraction_reason=None, **kwargs):
    """ Formats data for Retraction as dict object

        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        false_mgs_id : `str`
            The id of the message that is falsely published
        which_tier : 'str'
            OBS type of false message ['CoincidenceTier', 'SigTier', 'TimeTier, 'ALL']
        n_retract_latest: 'int' or 'str'
            Tells retraction methods to look for N  latest message sent by a detector. can also pass 'ALL'
            to retract all messages in a OBS tier.
        retraction_reason: 'str"
            Reason for message(s) retraction
        **kwargs
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            retraction_dict : `dict`
                dictionary of the retraction data

    """
    keys = ['machine_time', 'false_id',
            'N_retract_latest', 'which_tier', 'retraction_reason']
    values = [machine_time, false_mgs_id, n_retract_latest,
              which_tier, retraction_reason]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    retraction_dict = dict(zip_iterator)
    return retraction_dict


def heartbeat_data(machine_time=None,
                   detector_status=None, **kwargs):
    """ Formats data for Heartbeat as dict object

        Parameters
        ----------
        machine_time : `datetime`
            The machine time at the time of execution of command
        detector_status : 'str'
            ON or OFF
        **kwargs
            Any other key-value pair desired to be published. Notice,
            these additional arguments will be prepended with ^.

        Returns
        -------
            heartbeat_dict : `dict`
                dictionary of the Heartbeat data

    """
    keys = ['machine_time', 'detector_status']
    values = [machine_time, detector_status]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    heartbeat_dict = dict(zip_iterator)
    return heartbeat_dict

def _check_cli_request(requested, experiment, env):
    """ check the requested tier in the CLI
        Parameters
        ----------
        requested : `list`
            The list of requested tiers
        experiment : `str`
    """
    from . import hop_pub
    import numpy as np
    click.secho('\nRequested tiers are; ', bold=True)
    valid_tiers = ['coincidence','significance','timing']
    confused_ones = ['retraction', 'heartbeat', 'hb']
    publishers, names = [], []
    for i, tier in enumerate(requested):
        tier = tier.lower()
        if len(tier) == 1:
            if tier == 'c': tier = 'coincidence'
            if tier == 's': tier = 'significance'
            if tier == 't': tier = 'timing'
        if tier not in valid_tiers:
            if tier in confused_ones:
                click.secho(f'\t\t{tier} has its own separate function ! ', fg='yellow', bold=True)
                if i == len(requested): return None
            else:
                click.secho(f'\t\t{tier} << Not a valid tier! ' , fg='red', bold=True)
                if i == len(requested): return None
        else:
            click.secho(f'\t\t{tier}', fg='blue')

        if tier == 'coincidence':
            pub = hop_pub.Publisher_Coincidence_Tier(experiment, env).send_coincidence_tier_message
            name = tier
        if tier == 'significance':
            pub = hop_pub.Publisher_Significance_Tier(experiment, env).send_sig_tier_message
            name = tier
        if tier == 'timing':
            pub = hop_pub.Publisher_Timing_Tier(experiment, env).send_t_tier
            name = tier

        if tier in valid_tiers and name not in names:
            publishers.append(pub)
            names.append(name)
    return publishers, names

def _parse_file(filename):
    """ Parse the file to fetch the json data

    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return data





