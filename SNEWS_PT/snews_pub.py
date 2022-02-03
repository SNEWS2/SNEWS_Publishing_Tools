"""
An interface for SNEWS member experiment 
to publish their observation and heartbeat messages.

Created: 
August 2021
Authors: 
Melih Kara
Sebastian Torres-Lara
"""

# TODO: based on this post and its answers https://stackoverflow.com/questions/55099243/python3-dataclass-with-kwargsasterisk
# We can add a class method and allow for entries using ".from_kwargs/ from_dict" which then passes only the
# relevant fields to Tiers and displays/stores or appends extra fields
# Not sure if we should do this. As it still requires, user to know what is not needed and pass via this .from_kwargs
# I already implemented the functionality down; see commented-out parts

import os, click
from hop import Stream
from . import snews_pt_utils
from .message_schema import Message_Schema
from dataclasses import dataclass
import inspect, sys

class Publisher:
    """Class in charge of publishing messages to SNEWS-hop sever.
    This class acts as a context manager.

    Parameters
    ----------
    env_path: 'str'
        path to SNEWS env file, defaults to tes_config.env if None is passed.
    verbose: `bool`
        Option to display message when publishing.
    auth: `bool`
        Option to run hop-Stream without authentication. Pass False to do so
    """

    def __init__(self, env_path=None, verbose=True, auth=True):
        snews_pt_utils.set_env(env_path)
        self.auth = auth
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        self.times = snews_pt_utils.TimeStuff()
        self.verbose = verbose

    def __enter__(self):
        self.stream = Stream(until_eos=True, auth=self.auth).open(self.obs_broker, 'w')
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

        self.stream.write(message)
        self.display_message(message)

    def display_message(self, message):
        if self.verbose:
            click.secho(f'{"-" * 64}', fg='bright_blue')
            if message['_id'].split('_')[1] == 'FalseOBS':
                click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
            for k, v in message.items():
                print(f'{k:<20s}:{v}')


class CoincidenceTier:
    """CoincidenceTier
    Container class for CoincidenceTier, takes in message info and sets up schema.

    Attributes
    ----------
    p_value: `float`
        p-value of nu signal.
    neutrino_time: `str`
        nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    detector_name:  `str`, optional
        Name of your detector. default set by environment file
        Use snews_pt_utils.retrieve_detectors() to see the available detector names.
    machine_time: `str`
        time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    **kwargs:
        any key-value pairs that you want to pass
        These will be stored as meta-data if they are not larger than 2048 bytes
        They do not appear in the alert messages (#ToDo: pass them to experiments?)
    """
    def __init__(self, p_value, neutrino_time,
                 detector_name = os.getenv('DETECTOR_NAME'),
                 machine_time = None, **kwargs):
        self.p_value = p_value
        self.neutrino_time = neutrino_time
        self.detector_name = detector_name
        self.machine_time = machine_time
        self.kwargs = dict(kwargs)

    def message(self):
        """ Formats message structure

        returns
        -------
        message as dict object

        """
        # deal with the meta-data
        meta = {k: v for k, v in self.kwargs.items() if sys.getsizeof(v) < 2048}
        if len(meta):
            click.echo(click.style('\t"'+'; '.join(meta.keys())+'"', fg='magenta', bold=True) +' are passed as meta data')

        # deal with the data
        data = snews_pt_utils.coincidence_tier_data(machine_time=self.machine_time,
                                                    p_value=self.p_value,
                                                    nu_time=self.neutrino_time,
                                                    meta=meta,
                                                    )
        times = snews_pt_utils.TimeStuff()
        return Message_Schema(detector_key=self.detector_name).get_schema(message_type='CoincidenceTier', data=data,
                                                                             sent_time=times.get_snews_time())


class SignificanceTier:
    """SignificanceTier
       Container class for SignificanceTier, takes in message info and sets up schema.

       Attributes
       ----------
       neutrino_time: `str`
           nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       p_values: list of float
           p-values for a SN nu flux.
       detector_name:  `str`, optional
           Name of your detector. default set by environment file
           Use snews_pt_utils.retrieve_detectors() to see the available detector names.
       machine_time: `str`
           time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
       message_type: `str` (default:'SigTier')
           Name of tier, used to format the schema
       **kwargs:
           any key-value pairs that you want to pass
           These will be stored as meta-data if they are not larger than 2048 bytes
           They do not appear in the alert messages (#ToDo: pass them to experiments?)
       """
    def __init__(self, p_values, neutrino_time,
                 detector_name = os.getenv('DETECTOR_NAME'),
                 machine_time = None, **kwargs):
        self.p_values = p_values
        self.neutrino_time = neutrino_time
        self.detector_name = detector_name
        self.machine_time = machine_time
        self.kwargs = dict(kwargs)

    def message(self):
        """ Formats message structure

           returns
           -------
           message as dict object

        """
        # deal with the meta-data
        meta = {k: v for k, v in self.kwargs.items() if sys.getsizeof(v) < 2048}
        if len(meta):
            click.echo(
                click.style('\t"' + '; '.join(meta.keys()) + '"', fg='magenta', bold=True) + ' are passed as meta data')

        # deal with the data
        data = snews_pt_utils.sig_tier_data(machine_time=self.machine_time,
                                            nu_time=self.neutrino_time,
                                            p_values=self.p_values,
                                            meta=meta,
                                            )
        times = snews_pt_utils.TimeStuff()
        return Message_Schema(detector_key=self.detector_name).get_schema(message_type='SigTier', data=data,
                                                                          sent_time=times.get_snews_time())


class TimingTier:
    """Timing Tier
          Container class for Timing Tier, takes in message info and sets up schema.

          Attributes
          ----------
          nu_time: `str`
            nu arrival time. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          timing_series: list of str
              nu arrival times. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          detector_name:  `str`, optional
              Name of your detector. default set by environment file
              Use snews_pt_utils.retrieve_detectors() to see the available detector names.
          machine_time: `str`
              time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
          message_type: `str` (default:'SigTier')
              Name of tier, used to format the schema
          **kwargs:
           any key-value pairs that you want to pass
           These will be stored as meta-data if they are not larger than 2048 bytes
           They do not appear in the alert messages (#ToDo: pass them to experiments?)

          """
    def __init__(self,
                 timing_series,
                 neutrino_time,
                 detector_name = os.getenv('DETECTOR_NAME'),
                 machine_time = None, **kwargs):
        self.timing_series = timing_series
        self.neutrino_time = neutrino_time
        self.detector_name = detector_name
        self.machine_time = machine_time
        self.meta = {}
        self.kwargs = dict(kwargs)

    def message(self):
        """ Formats message structure

           returns
           -------
           message as dict object

        """
        # deal with the meta-data
        meta = {k: v for k, v in self.kwargs.items() if sys.getsizeof(v) < 2048}
        if len(meta):
            click.echo(
                click.style('\t"' + '; '.join(meta.keys()) + '"', fg='magenta', bold=True) + ' are passed as meta data')

        # deal with the data
        data = snews_pt_utils.time_tier_data(machine_time=self.machine_time,
                                             nu_time=self.neutrino_time,
                                             timing_series=self.timing_series,
                                             meta=meta
                                             )
        times = snews_pt_utils.TimeStuff()
        return Message_Schema(detector_key=self.detector_name).get_schema(message_type='TimeTier', data=data,
                                                                          sent_time=times.get_snews_time())


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
    detector_name:  str, Optional
        Name of your detector. default set by environment file
        Use snews_pt_utils.retrieve_detectors() to see the available detector names.
    message_type: str (default: 'FalseOBS'
        Set message type for schema
    machine_time: str (default: None)
        time recorded by detector. formats %y/%m/%d_%H:%M:%S:%f or %H:%M:%S:%f
    false_mgs_id: str (default: None)
        specific id of message you want to retract.
    retraction_reason: str (default: None)
        Reason why you are retracting.
    meta: dict (default: None)
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
    meta: dict = None

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
        machine time : `str`
            The time of submission of the message.
        detector_name: `str`, optional
            name of the detector, default set by environment file
    """
    status: str
    machine_time: str = None
    detector_name: str = os.getenv('DETECTOR_NAME')


    def message(self):
        status = self.status.upper()
        if status not in ["ON", "OFF"]:
            click.echo(f"{status} has to be 'ON' or 'OFF'\n\tSetting it to " + click.style('OFF', fg='red'))
            status = "OFF"

        data = snews_pt_utils.heartbeat_data(detector_status=status, machine_time=self.machine_time)
        message = Message_Schema(detector_key=self.detector_name).get_schema(message_type='Heartbeat',
                                                                             data=data, sent_time='')
        return message
