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


class SNEWSTiers:
    def __init__(self, detector_name=None, machine_time=None, nu_time=None, p_value=None,
                 p_values=None, timing_series=None, which_tier=None,
                 n_retract_latest=0, retraction_reason=None, detector_status=None, is_pre_sn=False, **kwargs):
        self.machine_time = machine_time
        self.nu_time = nu_time
        self.p_value = p_value
        self.p_values = p_values
        self.timing_series = timing_series
        self.which_tier = which_tier
        self.n_retract_latest = n_retract_latest
        self.retraction_reason = retraction_reason
        self.detector_status = detector_status
        self.is_pre_sn = is_pre_sn
        self.detector_name = detector_name
        if detector_name is None:
            self.detector_name = os.getenv('DETECTOR_NAME')
        self.kwargs = dict(kwargs)
        self.schema = Message_Schema(detector_key=self.detector_name, is_pre_sn=is_pre_sn)

    def determine_tier(self, ):
        messages = []
        meta = {k: v for k, v in self.kwargs.items() if sys.getsizeof(v) < 2048}
        if len(meta):
            click.echo(
                click.style('\t"' + '; '.join(meta.keys()) + '"', fg='magenta', bold=True) + ' are passed as meta data')

        if self.is_pre_sn and type(self.timing_series) == list:
            data = snews_pt_utils.time_tier_data(machine_time=self.machine_time,
                                                 nu_time=self.nu_time,
                                                 timing_series=self.timing_series,
                                                 p_val=self.p_value,
                                                 meta=meta
                                                 )

            time_message = self.schema.get_schema(tier='TimeTier', data=data, )
            messages.append(time_message)
            return messages
        # TODO: 16/02 ask about p val in CT
        # CoincidenceTier if it has p_value and nu time
        if type(self.p_value) == float and type(self.nu_time) == str:
            data = snews_pt_utils.coincidence_tier_data(machine_time=self.machine_time, p_val=self.p_value,
                                                        nu_time=self.nu_time, meta=meta)
            coincidence_message = self.schema.get_schema(tier='CoincidenceTier', data=data, )
            messages.append(coincidence_message)

        # SignificanceTier if it has p_values
        if type(self.p_values) == list:
            data = snews_pt_utils.sig_tier_data(machine_time=self.machine_time,
                                                nu_time=self.nu_time,
                                                p_values=self.p_values,
                                                meta=meta,
                                                )
            sig_message = self.schema.get_schema(tier='SigTier', data=data, )
            messages.append(sig_message)

        # TimingTier if timing_series exists (@Seb why do we need p_value to be float?)
        if type(self.timing_series) == list and type(self.p_value) == float:
            data = snews_pt_utils.time_tier_data(machine_time=self.machine_time,
                                                 nu_time=self.nu_time,
                                                 timing_series=self.timing_series,
                                                 p_val=self.p_value,
                                                 meta=meta
                                                 )

            time_message = self.schema.get_schema(tier='TimeTier', data=data, )
            messages.append(time_message)

        # Retraction Command if retraction field is passed
        if self.n_retract_latest != 0 and type(self.which_tier) == str:
            data = snews_pt_utils.retraction_data(machine_time=self.machine_time,
                                                  which_tier=self.which_tier, n_retract_latest=self.n_retract_latest,
                                                  retraction_reason=self.retraction_reason, meta=meta)
            retraction_message = self.schema.get_schema(tier='Retraction', data=data, )
            messages.append(retraction_message)

        # Heartbeat if detector status passed (and maybe other==None ?)
        # they can also set status=ON when they submit coincidence, do we want to publish also a HB at the same time?
        if type(self.detector_status) == str and type(self.machine_time) == str:
            data = snews_pt_utils.heartbeat_data(detector_status=self.detector_status, machine_time=self.machine_time)
            heartbeat_message = self.schema.get_schema(tier='Heartbeat', data=data, )
            messages.append(heartbeat_message)

        return messages
