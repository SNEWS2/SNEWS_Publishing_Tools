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
from dataclasses import dataclass


class Publisher:
    def __init__(self, env_path=None):
        snews_pt_utils.set_env(env_path)
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.times = snews_pt_utils.TimeStuff()

    def send(self, message):
        stream = Stream(persist=False)
        message['sent_time'] = self.times.get_snews_time()
        with stream.open(self.obs_broker, 'w') as s:
            s.write(message)
        click.secho(f'{"-" * 57}', fg='bright_blue')
        if message['_id'].split('_') == 'FalseOBS':
            click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
        for k, v in message.items():
            print(f'{k:<20s}:{v}')


@dataclass
class CoincidenceTier:
    """CoincidenceTier
    Container class for CoincidenceTier, takes in message info and sets up schema.

    Attributes
    ----------
    detector_name:  str
        Name of your detector.
        Use snews_pt_utils.retrieve_detectors() to see the available detector names.
    p_val: float
        p-value of nu signal.
    nu_time: str
        nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    machine_time: str
        time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    message_type: str (default:'CoincidenceTier')
        Name of tier, used to format the schema
    extra: dict (default: None)
        Use this in case you want to send extra information.
        Make sure it's formatted as a dict.

    """
    detector_name: str
    p_val: float
    nu_time: str
    machine_time: str = None
    message_type: str = 'CoincidenceTier'
    extra: dict = None

    def message(self):
        """
        Formats message structure

        returns
        -------
        message as dict object

        """
        data = snews_pt_utils.coincidence_tier_data(machine_time=self.machine_time,
                                                    p_value=self.p_val,
                                                    nu_time=self.nu_time,
                                                    )
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.coincidence_tier_data(**self.extra, machine_time=self.machine_time,
                                                        p_value=self.p_val,
                                                        nu_time=self.nu_time,
                                                        )

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


@dataclass
class SignificanceTier:
    """SignificanceTier
       Container class for SignificanceTier, takes in message info and sets up schema.

       Attributes
       ----------
       detector_name:  str
           Name of your detector.
           Use snews_pt_utils.retrieve_detectors() to see the available detector names.
       p_values: list of float
           p-values for a SN nu flux.
       nu_time: str
           nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       machine_time: str
           time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       message_type: str (default:'SigTier')
           Name of tier, used to format the schema
       extra: dict (default: None)
           Use this in case you want to send extra information.
           Make sure it's formatted as a dict.

       """
    detector_name: str
    nu_time: str
    p_values: list
    machine_time: str = None
    extra: dict = None
    message_type: str = 'SigTier'

    def message(self):
        """
           Formats message structure

           returns
           -------
           message as dict object

           """
        data = snews_pt_utils.sig_tier_data(machine_time=self.machine_time, nu_time=self.nu_time,
                                            p_values=self.p_values)
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.sig_tier_data(**self.extra, machine_time=self.machine_time, nu_time=self.nu_time,
                                                p_values=self.p_values)

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


@dataclass
class TimingTier:
    """Timing Tier
          Container class for Timing Tier, takes in message info and sets up schema.

          Attributes
          ----------
          detector_name:  str
              Name of your detector.
              Use snews_pt_utils.retrieve_detectors() to see the available detector names.
          nu_time: str
            nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          timing_series: list of str
              nu arrival times. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          machine_time: str
              time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          message_type: str (default:'SigTier')
              Name of tier, used to format the schema
          extra: dict (default: None)
              Use this in case you want to send extra information.
              Make sure it's formatted as a dict.

          """
    detector_name: str
    nu_time: str
    timing_series: list
    machine_time: str = None
    extra: dict = None
    message_type: str = 'TimeTier'

    def message(self):
        """
           Formats message structure

           returns
           -------
           message as dict object

           """
        data = snews_pt_utils.time_tier_data(machine_time=self.machine_time, nu_time=self.nu_time,
                                             timing_series=self.timing_series, )
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.time_tier_data(machine_time=self.machine_time, nu_time=self.nu_time,
                                                 timing_series=self.timing_series,
                                                 **self.extra)

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


@dataclass
class Retraction:
    """Retraction
    Container class for retraction messages.
    Attributes
    ----------
    detector_name:  str
        Name of your detector.
        Use snews_pt_utils.retrieve_detectors() to see the available detector names.
    which_tier: str
        Name of tier you want to retract from,
            'CoincidenceTier'
            'SigTier'
            'TimeTier'
    n_retract_latest: int
        Number of most recent message you want to retract
    message_type: str (default: 'FalseOBS'
        Set message type for schema
    machine_time: str (default: None)
        time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    false_mgs_id: str (default: None)
        specific id of message you want to retract.
    retraction_reason: str (default: None)
        Reason why you are retracting.
    extra: dict (default: None)
        Use this in case you want to send extra information.
        Make sure it's formatted as a dict!!!

    """
    detector_name: str
    which_tier: str
    n_retract_latest: int
    message_type: str = 'FalseOBS'
    machine_time: str = None
    false_mgs_id: str = None
    retraction_reason: str = None
    extra: dict = None
    def message(self):
        """
           Formats message structure

           returns
           -------
           message as dict object

           """
        data = snews_pt_utils.retraction_data(machine_time=self.machine_time, false_mgs_id=self.false_mgs_id,
                                              which_tier=self.which_tier, n_retract_latest=self.n_retract_latest,
                                              retraction_reason=self.retraction_reason, )
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.retraction_data(machine_time=self.machine_time, false_mgs_id=self.false_mgs_id,
                                                  which_tier=self.which_tier, n_retract_latest=self.n_retract_latest,
                                                  retraction_reason=self.retraction_reason, **self.extra)

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


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

    def send_HBs(self, path_to_log=None):
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
