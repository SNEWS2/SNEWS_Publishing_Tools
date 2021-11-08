"""
Example initial dosctring
"""
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple
import os, json
from pathlib import Path
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
    default_env_path = os.path.dirname(__file__) + '/auxiliary/test-config.env'
    env = env_path or default_env_path
    load_dotenv(env)


def make_dir(path):
    """ make a directory in a given path """
    if Path(path).is_dir():
        pass
    else:
        os.makedirs(path)


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


def get_logger(scriptname, logfile_name):
    """ Logger

    .. note:: Deprecated

    """
    import logging
    # Gets or creates a logger
    logger = logging.getLogger(scriptname)

    # set log level
    logger.setLevel(logging.INFO)
    # define file handler and set formatter
    file_handler = logging.FileHandler(logfile_name)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    # add file handler to logger
    logger.addHandler(file_handler)
    return logger


def display_gif():
    """ Some fun method to display an alert gif
        If running on notebook

    """
    if isnotebook():
        from IPython.display import HTML, display
        giphy_snews = "https://raw.githubusercontent.com/SNEWS2/hop-SNalert-app/snews2_dev/hop_comms/auxiliary/snalert.gif"
        display(HTML(f'<img src={giphy_snews}>'))


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
        detector_status : `str`
            ON/OFF depending on the detector status
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
    keys = ['machine_time', 'neutrino_time', 'p_value', 'timing_series', 'detector_status', 'false_id',
            'N_retract_latest', 'which_tier', 'retraction_reason']
    values = [machine_time, nu_time, p_value, timing_series, detector_status, false_mgs_id, N_retract_latest,
              which_tier, retraction_reason]
    # allow for keyword-args
    for k, v in kwargs.items():
        keys.append(k)
        values.append(v)
    zip_iterator = zip(keys, values)
    data_dict = dict(zip_iterator)
    return data_dict


def data_alert(p_vals=None, detector_events=None, t_series=None, nu_times=None,
               ids=None, locs=None, status=None, machine_times=None):
    """ Default alert message data
        
        Parameters
        ----------
        p_vals : `list`
            list with p-values of the observations involved in the alert
        detectors_events : `dict`
            dict of detectors and their number of events involved in the alert
        t_series : `list`
            list of timeseries (if applicable)
        nu_time : `list`
            list of neutrino arrival times
        ids : `list`
            list of ids of the detectors involved in the alert
        locs : `list`
            list of locations of the experiments involved in the alert
        status : `list`
            Depracted?              
        machine_times : `list`
            The machine times of the experiments involved in the alert

        Returns        
        -------
            `dict`
                dictionary of the complete alert data

    """
    keys = ['p_vals', 'detector_events', 't_series', 'neutrino_times', 'ids', 'locs', 'status', 'machine_times']
    values = [p_vals, detector_events, t_series, nu_times, ids, locs, status, machine_times]
    return dict(zip(keys, values))

# Note from from Seb: :(
## Not working properly
# def run_parallel(nparallel=2):
#     """ Run publish & subscribe methods in parallel
#         Only works for notebooks. Requires ipyparallel
#         Arguments
#         ---------
#         nparallel : int
#             number of cells to run in parallel
#     """
#     if not isnotebook():
#         import sys
#         sys.exit('Cannot run processes in parallel')
#     # enable the extension in the current environment
#     os.system('ipcluster nbextension enable --user')
#     os.system(f'ipcluster start -n {nparallel}')
#     from ipyparallel import Client
#     rc = Client()
#     print("Run `%%px -a -t 0` magic command on the notebook!")
#     return None
