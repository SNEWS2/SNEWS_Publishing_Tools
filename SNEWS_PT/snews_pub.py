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

    def send(self, messages):
        """This method will set the sent_time and send the message to the hop broker.

        Parameters
        ----------
        messages: list
            list containing observation message.

        """
        for message in messages:
            self.stream.write(message)
            self.display_message(message)

    def display_message(self, message):
        if self.verbose:
            tier = message['_id'].split('_')[1]
            click.secho(f'{"-" * 64}', fg='bright_blue')
            click.secho(f'Sending message to {tier}', fg='bright_red')
            if tier == 'Retraction':
                click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
            for k, v in message.items():
                print(f'{k:<20s}:{v}')


class SNEWSTiersPublisher:
    """
    To use a json file call SNEWSTiersPublisher().from_json(<filename>)
    Else, the following keys and more kwargs can be passed
      `detector_name`
      `machine_time`
      `nu_time`
      `p_val`
      `p_values`
      `timing_series`
      `which_tier`
      `n_retract_latest`
      `retraction_reason`
      `detector_status`
      `is_pre_sn`
    """
    def __init__(self, env_file=None, **kwargs):
        self.args_dict = dict(**kwargs)
        self.env_file = env_file
        self.messages, self.tiernames = snews_pt_utils._tier_decider(self.args_dict, env_file)

    def from_json(self, jsonfile):
        """ Read the data from a json file

        """
        input_json = snews_pt_utils._parse_file(jsonfile)
        self.args_dict = input_json
        self.messages, self.tiernames = snews_pt_utils._tier_decider(input_json, self.env_file)

    def send_to_snews(self):
        with Publisher() as pub:
            pub.send(self.messages)
