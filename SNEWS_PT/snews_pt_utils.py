"""
Utility tools for SNEWS_PT
"""
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple
import os, json, click
import sys


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
    detectors_path : `str`
        path for the json file with all detectors. By default this is
        /auxiliary/detector_properties.json

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


def coincidence_tier_data(machine_time=None, nu_time=None, p_val=None, meta=None):
    """ Formats data for CoincidenceTier as dict object

        Parameters
        ----------
        machine_time : `str`
            The machine time at the time of execution of command
        nu_time : `str`
            The neutrino arrival time
        p_val : `float`
            If determined, the p value of the observation
        meta : `dict`
            Any other key-value pair desired to be published.

        Returns
        -------
            coincidence_tier_dict : `dict`
                dictionary of the complete CoincidenceTier data

    """
    keys = ['machine_time', 'neutrino_time', 'p_value', 'meta']
    values = [machine_time, nu_time, p_val, meta]
    zip_iterator = zip(keys, values)
    coincidence_tier_dict = dict(zip_iterator)
    return coincidence_tier_dict


def sig_tier_data(machine_time=None, nu_time=None, p_values=None, meta=None):
    """ Formats data for SigTier as dict object

        Parameters
        ----------
        machine_time : `str`
            The machine time at the time of execution of command
        nu_time : `str`
            The neutrino arrival time
        p_values : `list`
            If determined, the p values of the observation
        meta : `dict`
            Any other key-value pair desired to be published.

        Returns
        -------
            sig_tier_dict : `dict`
                dictionary of the complete observation data

    """
    keys = ['machine_time', 'neutrino_time', 'p_values', 'meta']
    values = [machine_time, nu_time, p_values, meta]
    zip_iterator = zip(keys, values)
    sig_tier_dict = dict(zip_iterator)
    return sig_tier_dict


def time_tier_data(machine_time=None, nu_time=None, p_val=None, timing_series=None, meta=None):
    """ Formats data for TimingTier as dict object

        Parameters
        ----------
        machine_time : `str`
            The machine time at the time of execution of command
        nu_time : `str`
            The neutrino arrival time
        timing_series : `array-like`
            Time series of the detected signal
        meta : `dict`
            Any other key-value pair desired to be published.

        Returns
        -------
            data_dict : `dict`
                dictionary of the TimingTier data

    """
    keys = ['machine_time', 'neutrino_time', 'timing_series', 'p_val', 'meta']
    values = [machine_time, nu_time, timing_series, p_val, meta]
    zip_iterator = zip(keys, values)
    time_tier_dict = dict(zip_iterator)
    return time_tier_dict


def retraction_data(machine_time=None, which_tier=None,
                    n_retract_latest=0, retraction_reason=None, meta=None):
    """ Formats data for Retraction as dict object

        Parameters
        ----------
        machine_time : `str`
            The machine time at the time of execution of command
        which_tier : 'str'
            OBS type of false message ['CoincidenceTier', 'SigTier', 'TimeTier, 'ALL']
        n_retract_latest: 'int' or 'str'
            Tells retraction methods to look for N  latest message sent by a detector. can also pass 'ALL'
            to retract all messages in a OBS tier.
        retraction_reason: 'str"
            Reason for message(s) retraction
       meta : `dict`
            Any other key-value pair desired to be published.


        Returns
        -------
            retraction_dict : `dict`
                dictionary of the retraction data

    """
    keys = ['machine_time',
            'N_retract_latest', 'which_tier', 'retraction_reason', 'meta']
    values = [machine_time, n_retract_latest,
              which_tier, retraction_reason, meta]
    zip_iterator = zip(keys, values)
    retraction_dict = dict(zip_iterator)
    return retraction_dict


def heartbeat_data(machine_time=None,
                   detector_status=None, meta=None):
    """ Formats data for Heartbeat as dict object

        Parameters
        ----------
        machine_time : `str`
            The machine time at the time of execution of command
        detector_status : 'str'
            ON or OFF
         meta : `dict`
            Any other key-value pair desired to be published.

        Returns
        -------
            heartbeat_dict : `dict`
                dictionary of the Heartbeat data

    """
    keys = ['machine_time', 'detector_status', 'meta']
    values = [machine_time, detector_status, meta]

    zip_iterator = zip(keys, values)
    heartbeat_dict = dict(zip_iterator)
    return heartbeat_dict


def _check_aliases(tier):
    tier = tier.lower()
    coincidence_aliases = ['coincidence', 'c', 'coincidencetier', 'coinc']
    significance_aliases = ['significance', 's', 'significancetier', 'sigtier']
    timing_aliases = ['timing', 'time', 'timingtier', 'timetier', 't']
    false_aliases = ['false', 'falseobs', 'retraction', 'retract', 'r', 'f']
    heartbeat_aliases = ['heartbeat', 'hb']

    if tier in coincidence_aliases:
        tier = 'CoincidenceTier'
    elif tier in significance_aliases:
        tier = 'SigTier'
    elif tier in timing_aliases:
        tier = 'TimeTier'
    elif tier in false_aliases:
        tier = 'FalseOBS'
    elif tier in heartbeat_aliases:
        tier = 'Heartbeat'
    else:
        click.secho(f'"{tier}" <- not a valid argument!', fg='bright_red')
        sys.exit()
    return [tier]


# def _check_cli_request(requested):
#     """ check the requested tier in the CLI
#
#         Parameters
#         ----------
#         requested : `list`
#             The list of requested tiers
#
#     """
#     from .snews_pub import SNEWSTiers
#
#     valid_tiers_names = ['CoincidenceTier', 'SigTier', 'TimeTier']
#     valid_tiers = [CoincidenceTier, SignificanceTier, TimingTier]
#     tier_pairs = dict(zip(valid_tiers_names, valid_tiers))
#     other_tiers_names = ['Heartbeat', 'FalseOBS']
#     other_tiers = [Heartbeat, Retraction]
#     other_pairs = dict(zip(other_tiers_names, other_tiers))
#
#     tier_name_pair = []
#     click.secho('\nRequested tiers are; ', bold=True)
#     for i, tier in enumerate(requested):
#         tier = tier.lower()
#         tiername = _check_aliases(tier)[0]
#         if tiername in valid_tiers_names:
#             tier_name_pair.append((tier_pairs[tiername], tiername))
#         elif tiername in other_tiers_names:
#             click.echo(click.style(f'\t\t> {tiername}\n', fg='yellow', bold=True) +
#                        '\t\t    has its own separate function !\n'
#                        f'\t\t    See ' + click.style(f'{other_pairs[tiername]}', fg='yellow'))
#             if i == len(requested): return None
#         else:
#             return None
#
#     tiers_unique, names_unique = [], []
#     for Tier, name in tier_name_pair:
#         if name not in names_unique:
#             names_unique.append(name)
#             tiers_unique.append(Tier)
#             click.secho(f'\t\t> {name}', fg='cyan')
#     return tiers_unique, names_unique


def _tier_decider(data:dict) -> tuple:
    """ Decide on the tier(s) or commands (Heartbeat/Retraction)
        Based on the content of the message

    """
    from .snews_pub import SNEWSTiers
    from inspect import signature
    from .message_schema import Message_Schema

    detector_name = data.get('detector_name', os.getenv("DETECTOR_NAME"))
    is_pre_sn = bool(data.get('is_pre_sn', 'False'))
    schema = Message_Schema(detector_key=detector_name, is_pre_sn=is_pre_sn)

    keys_valid = list(signature(SNEWSTiers).parameters.keys())
    keys_valid.remove('kwargs')

    # if there are keys that wouldn't belong to any tier/command pass them as meta
    meta_keys = [key for key,value in data.items() if sys.getsizeof(value) < 2048]
    meta_data = {k:data[k] for k in meta_keys}

    messages, tiernames = [], []
    def _append_messages(tier_function, name):
        tier_keys = list(signature(tier_function).parameters.keys())
        data_for_tier = {k: v for k, v in data.items() if k in tier_keys}
        if name not in ['Retraction','Heartbeat']:
            data_for_tier['meta'] = meta_data
        msg =  schema.get_schema(tier=name, data=data_for_tier, )
        messages.append(tier_function(**msg))
        tiernames.append(name)

    # if is_pre_sn:
    #     print('This is a pre-supernova message')
    #     _append_messages(time_tier_data, 'TimingTier')

    # CoincidenceTier if it has p_value
    if type(data.get('p_val', False))==float:
        _append_messages(coincidence_tier_data,'CoincidenceTier')

    # SignificanceTier if it has p_values
    if data.get('p_values', False):
        _append_messages(sig_tier_data,'SignificanceTier')

    # TimingTier if timing_series exists (@Seb why do we need p_value to be float?)
    if data.get('timing_series', False):
        _append_messages(time_tier_data, 'SignificanceTier')

    # asking which tier doesn't make sense if the user doesn't know the tiers
    if data.get('n_retract_latest', False):
        _append_messages(retraction_data, 'Retraction')

    if data.get('detector_status', False):
        _append_messages(heartbeat_data, 'Heartbeat')
    return tiernames, messages


def _parse_file(filename):
    """ Parse the file to fetch the json data

    Notes
    -----
    Infer Tier based on keys ?
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def isnotebook():
    """ Tell if the script is running on a notebook

    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def display_gif():
    """ Some fun method to display an alert gif
        If running on notebook.

    """
    if isnotebook():
        from IPython.display import HTML, display
        giphy_snews = "https://raw.githubusercontent.com/SNEWS2/hop-SNalert-app/snews2_dev/hop_comms/auxiliary/snalert.gif"
        display(HTML(f'<img src={giphy_snews}>'))
