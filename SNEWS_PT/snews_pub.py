"""
An interface for SNEWS member experiment 
to publish their observation and heartbeat messages.

Created: 
August 2021
Authors: 
Melih Kara
Sebastian Torres-Lara
"""
import os, click
from hop import Stream
from . import snews_pt_utils
from .message_schema import Message_Schema
from dataclasses import dataclass
import inspect


class Publisher:
    """Class in charge of publishing messages to SNEWS-hop sever.
    This class acts as a context manager.

    Parameters
    ----------
    env_path: 'str'
        path to SNEWS env file, defaults to tes_config.env if None is passed.
    verbose: bool
        Option to display message when publishing.
    """
    def __init__(self, env_path=None, verbose=True):
        snews_pt_utils.set_env(env_path)
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.times = snews_pt_utils.TimeStuff()
        self.verbose = verbose

    def __enter__(self):
        self.stream = Stream(until_eos=True).open(self.obs_broker, 'w')
        return self

    def __exit__(self, *args):
        self.stream.close()

    def send(self, message):
        """This method will set the sent_time and send the message to the hop broker.

        Parameters
        ----------
        message: dict
            observation message.

        """
        message['sent_time'] = self.times.get_snews_time()
        self.stream.write(message)
        self.display_message(message)


    def display_message(self, message):
        if self.verbose:
            click.secho(f'{"-" * 57}', fg='bright_blue')
            if message['_id'].split('_')[1] == 'FalseOBS':
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

    p_value: float
    neutrino_time: str
    detector_name: str = os.getenv('DETECTOR_NAME')
    machine_time: str = None
    message_type: str = 'CoincidenceTier'

    @classmethod
    def from_dict(cls, env):
        valid_data = cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
        for k,v in env.items():
            if k not in inspect.signature(cls).parameters:
                click.echo(click.style(k, fg='bright_red')+f' not a valid key for CoincidenceTier')
        return valid_data

    def message(self):
        """
        Formats message structure

        returns
        -------
        message as dict object

        """
        data = snews_pt_utils.coincidence_tier_data(machine_time=self.machine_time,
                                                    p_value=self.p_value,
                                                    nu_time=self.neutrino_time,
                                                    )
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.coincidence_tier_data(**self.extra, machine_time=self.machine_time,
                                                        p_value=self.p_value,
                                                        nu_time=self.neutrino_time,
                                                        )

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


@dataclass
class SignificanceTier:
    """SignificanceTier
       Container class for SignificanceTier, takes in message info and sets up schema.

       Attributes
       ----------
       nu_time: str
           nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       p_values: list of float
           p-values for a SN nu flux.
       detector_name:  str
           Name of your detector.
           Use snews_pt_utils.retrieve_detectors() to see the available detector names.
       machine_time: str
           time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       message_type: str (default:'SigTier')
           Name of tier, used to format the schema
       extra: dict (default: None)
           Use this in case you want to send extra information.
           Make sure it's formatted as a dict.

       """
    neutrino_time: str
    p_values: list
    detector_name: str = os.getenv('DETECTOR_NAME')
    machine_time: str = None
    extra: dict = None
    message_type: str = 'SigTier'

    @classmethod
    def from_dict(cls, env):
        valid_data = cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
        for k,v in env.items():
            if k not in inspect.signature(cls).parameters:
                click.echo(click.style(k, fg='bright_red')+f' not a valid key for SigTier')
        return valid_data

    def message(self):
        """
           Formats message structure

           returns
           -------
           message as dict object

           """
        data = snews_pt_utils.sig_tier_data(machine_time=self.machine_time, nu_time=self.neutrino_time,
                                            p_values=self.p_values)
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.sig_tier_data(**self.extra, machine_time=self.machine_time, nu_time=self.neutrino_time,
                                                p_values=self.p_values)

        return Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type, data=data,
                                                                          sent_time='')


@dataclass
class TimingTier:
    """Timing Tier
          Container class for Timing Tier, takes in message info and sets up schema.

          Attributes
          ----------
          nu_time: str
            nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          timing_series: list of str
              nu arrival times. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          detector_name:  str
              Name of your detector.
              Use snews_pt_utils.retrieve_detectors() to see the available detector names.
          machine_time: str
              time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          message_type: str (default:'SigTier')
              Name of tier, used to format the schema
          extra: dict (default: None)
              Use this in case you want to send extra information.
              Make sure it's formatted as a dict.

          """
    neutrino_time: str
    timing_series: list
    detector_name: str = os.getenv('DETECTOR_NAME')
    machine_time: str = None
    extra: dict = None
    message_type: str = 'TimeTier'

    @classmethod
    def from_dict(cls, env):
        valid_data = cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
        for k,v in env.items():
            if k not in inspect.signature(cls).parameters:
                click.echo(click.style(k, fg='bright_red')+f' not a valid key for TimeTier')
        return valid_data

    def message(self):
        """
           Formats message structure

           returns
           -------
           message as dict object

           """
        data = snews_pt_utils.time_tier_data(machine_time=self.machine_time, nu_time=self.neutrino_time,
                                             timing_series=self.timing_series, )
        if self.extra != None and type(self.extra) == dict:
            data = snews_pt_utils.time_tier_data(machine_time=self.machine_time, nu_time=self.neutrino_time,
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
    which_tier: str
        Name of tier you want to retract from,
            'CoincidenceTier'
            'SigTier'
            'TimeTier'
    n_retract_latest: int
        Number of most recent message you want to retract
    detector_name:  str
        Name of your detector.
        Use snews_pt_utils.retrieve_detectors() to see the available detector names.
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
    which_tier: str
    n_retract_latest: int = 1
    detector_name: str = os.getenv('DETECTOR_NAME')
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


@dataclass
class Heartbeat:
    """ Publish Heartbeat message.
        We recommend submitting messages every 3 minutes
        Ideally, this function should be called after fetching
        the status of the detector

        Parameters
        ----------
        status : `str` ("ON"/"OFF")
            status of the detector at the time of invocation
        detector_name: `str`
            name of the detector
    """
    status: str
    detector_name: str = os.getenv('DETECTOR_NAME')
    machine_time: str = None
    extra: dict = None
    message_type: str = 'Heartbeat'

    def message(self):
        status = self.status.upper()
        if status not in ["ON", "OFF"]:
            click.echo(f"{status} has to be 'ON' or 'OFF'\n\tSetting it to " + click.style('OFF', fg='red'))
            status = "OFF"

        data = snews_pt_utils.heartbeat_data(detector_status=status, machine_time=self.machine_time)
        message = Message_Schema(detector_key=self.detector_name).get_schema(message_type=self.message_type,
                                                                             data=data, sent_time='')
        return message
