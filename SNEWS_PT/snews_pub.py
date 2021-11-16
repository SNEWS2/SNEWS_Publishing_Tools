"""
An interface for SNEWS member experiment 
to publish their observation and heartbeat messages.

Created: 
August 2021
Authors: 
Melih Kara
Sebastian Torres-Lara
"""
import hop, sys, time, os, json, click
from hop import Stream
from . import snews_pt_utils
from .message_schema import Message_Schema
import schedule



class Publisher_Coincidence_Tier:
    """ Publish Coincidence Tier message.

    Parameters
    ----------
    detector : `str`
            The name of the detector
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """
    def __init__(self, detector, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.times = snews_pt_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.msg_type = 'CoincidenceTier'
        self.schema = Message_Schema(detector_key=detector)

    def send_coincidence_tier_message(self, machine_time=None, nu_time=None, p_value=None, **kwargs):
        """ Publish message to stream

        Parameters
        ----------
        data : `dict`
            Data dictionary received from snews_utils.data()

        """
        data = snews_pt_utils.coincidence_tier_data(machine_time=machine_time, p_value=p_value, nu_time=nu_time,
                                                    **kwargs)
        sent_time = self.times.get_snews_time()
        obs_schema = self.schema.get_schema(message_type=self.msg_type, data=data, sent_time=sent_time)
        stream = Stream(persist=False)
        with stream.open(self.obs_broker, 'w') as s:
            s.write(obs_schema)
        click.secho(f'{"-" * 57}', fg='bright_blue')

        for k, v in obs_schema.items():
            print(f'{k:<20s}:{v}')


class Publisher_Significance_Tier:
    """ Publish Significance Tier message.

    Parameters
    ----------
    detector : `str`
            The name of the detector
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """
    def __init__(self, detector, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.times = snews_pt_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.msg_type = 'SigTier'
        self.schema = Message_Schema(detector_key=detector)

    def send_sig_tier_message(self, machine_time=None, nu_time=None, p_values=None, **kwargs):
        """ Publish message to stream

        Parameters
        ----------
        data : `dict`
            Data dictionary received from snews_utils.data()

        """
        data = snews_pt_utils.sig_tier_data(machine_time=machine_time, nu_time=nu_time, p_values=p_values, **kwargs)
        sent_time = self.times.get_snews_time()
        obs_schema = self.schema.get_schema(self.msg_type, data, sent_time)

        stream = Stream(persist=False)
        with stream.open(self.obs_broker, 'w') as s:
            s.write(obs_schema)
        click.secho(f'{"-" * 57}', fg='bright_blue')

        for k, v in obs_schema.items():
            print(f'{k:<20s}:{v}')


class Publisher_Timing_Tier:
    """ Publish Timig Tier message.

    Parameters
    ----------
    detector : `str`
            The name of the detector
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """
    def __init__(self, detector, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.times = snews_pt_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.msg_type = 'TimeTier'
        self.schema = Message_Schema(detector_key=detector)

    def send_t_tier(self, machine_time=None, nu_time=None, timing_series=None, **kwargs):
        """ Publish message to stream

        Parameters
        ----------
        data : `dict`
            Data dictionary received from snews_utils.data()

        """
        data = snews_pt_utils.time_tier_data(machine_time=machine_time, nu_time=nu_time, timing_series=timing_series,
                                             **kwargs)
        sent_time = self.times.get_snews_time()
        obs_schema = self.schema.get_schema(self.msg_type, data, sent_time)

        stream = Stream(persist=False)
        with stream.open(self.obs_broker, 'w') as s:
            s.write(obs_schema)
        click.secho(f'{"-" * 57}', fg='bright_blue')

        for k, v in obs_schema.items():
            print(f'{k:<20s}:{v}')


class Publisher_Rectraction:
    """ Publish Retraction message.

    Parameters
    ----------
    detector : `str`
            The name of the detector
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """
    def __init__(self, detector, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.times = snews_pt_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.msg_type = 'FalseOBS'
        self.schema = Message_Schema(detector_key=detector)

    def retract(self, machine_time=None, false_mgs_id=None, which_tier=None, n_retract_latest=0, retraction_reason=None,
                **kwargs):
        """ Publish retraction message to stream

        Parameters
        ----------
        data : `dict`
            Data dictionary received from snews_utils.data()

        """
        data = snews_pt_utils.retraction_data(machine_time=machine_time, false_mgs_id=false_mgs_id,
                                              which_tier=which_tier, n_retract_latest=n_retract_latest,
                                              retraction_reason=retraction_reason, **kwargs)
        sent_time = self.times.get_snews_time()
        obs_schema = self.schema.get_schema(message_type=self.msg_type, data=data, sent_time=sent_time)

        stream = Stream(persist=False)
        with stream.open(self.obs_broker, 'w') as s:
            s.write(obs_schema)
        click.secho(f'{"-" * 57}', fg='bright_blue')
        click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
        for k, v in obs_schema.items():
            print(f'{k:<20s}:{v}')


class Publisher_Heartbeat:
    """ Publish Heartbeat message.

    Parameters
    ----------
    detector : `str`
            The name of the detector
    env_path : `str`
        path for the environment file.
        Use default settings if not given

    """

    def __init__(self, detector, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.times = snews_pt_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.msg_type = 'Heartbeat'
        self.schema = Message_Schema(detector_key=detector)

    def send_HB(self, path_to_log=None):
        """ Publish  Heartbeat message to stream every 10 mins

        Parameters
        ----------
        data : `dict`
            Data dictionary received from snews_utils.data()

        """
        if path_to_log == None:
            path_to_log = './example_detector_log.json'
        with open(path_to_log) as log:
            log = json.load(log)
            detector_status = log['detector_status']
            machine_time = log['machine_time']
        sent_time = self.times.get_snews_time()
        data = snews_pt_utils.heartbeat_data(detector_status=detector_status, machine_time=machine_time)
        message_schema = self.schema.get_schema(message_type=self.msg_type, data=data, sent_time=sent_time)

        stream = Stream(persist=True)
        with stream.open(self.obs_broker, 'w') as s:
            schedule.every(10).minute.at(":00").do(s.write(message_schema))
