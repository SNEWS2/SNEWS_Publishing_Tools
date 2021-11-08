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
from . import snews_utils
from .hop_mgs_schema import Message_Schema




class Publish_Tier_Obs:
    """ Publish Supernova Observation messages to
        different tiers.
    
    Parameters
    ---------- 
    env_path : `str`
        path for the environment file.
        Use default settings if not given
    
    """

    def __init__(self, env_path=None):
        snews_utils.set_env(env_path)
        self.times = snews_utils.TimeStuff()
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")

    def publish(self, detector, msg_type, data):
        """ Publish message to stream

        Parameters
        ----------
        detector : `str`
            The name of the detector
        msg_type : `str`
            Type (Tier) of the message. Has to be one of 
            the 'CoincidenceTier', 'SigTier', 'TimeTier', 'FalseOBS'
        data : `dict`
            Data dictionary received from snews_utils.data_obs()

        """
        schema = Message_Schema(detector_key=detector)
        sent_time = self.times.get_snews_time()
        obs_schema = schema.get_obs_schema(msg_type, data, sent_time)

        stream = Stream(persist=False)
        with stream.open(self.obs_broker, 'w') as s:
            s.write(obs_schema)
        click.secho(f'{"-" * 57}', fg='bright_blue')
        if msg_type == 'FalseOBS':
            click.secho("It's okay, we all make mistakes".upper(),fg='magenta')
        for k, v in obs_schema.items():
            print(f'{k:<20s}:{v}')
