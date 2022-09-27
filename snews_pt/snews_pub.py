"""
An interface for SNEWS member experiment 
to publish their observation and heartbeat messages.

Created: 
August 2021
Authors: 
Melih Kara
Sebastian Torres-Lara
Joe Smolsky
"""

from datetime import datetime
import os, click
from hop import Stream
from . import snews_pt_utils


class Publisher:

    def __init__(self, env_path=None, verbose=True, auth=True, firedrill_mode=True):
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
        firedrill_mode :`bool`
            whether to use firedrill broker
        """
        snews_pt_utils.set_env(env_path)
        self.auth = auth
        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        if firedrill_mode:
            self.obs_broker = os.getenv("FIREDRILL_OBSERVATION_TOPIC")
        # self.times = snews_pt_utils.TimeStuff()
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
        if type(messages) == dict:
            messages = list(messages)
        for message in messages:
            if snews_pt_utils.is_snews_format(message):
                self.stream.write(message)
                self.display_message(message)
            else:
                click.secho(f'{"-" * 64}', fg='bright_red')
                click.secho(f'Skipping message! Improper format!')
                for k, v in message.items():
                    print(f'{k:<20s}:{v}')
            
    def display_message(self, message):
        if self.verbose:
            tier = message['_id'].split('_')[1]
            click.secho(f'{"-" * 64}', fg='bright_blue')
            click.secho(f'Sending message to {tier} on {self.obs_broker}', fg='bright_red')
            if tier == 'Retraction':
                click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
            for k, v in message.items():
                print(f'{k:<20s}:{v}')


class SNEWSTiersPublisher:

    def __init__(self, env_file=None,
                 detector_name='TEST',
                 machine_time=None,
                 neutrino_time=None,
                 p_val=None,
                 p_values=None,
                 t_bin_width=None,
                 timing_series=None,
                 which_tier=None,
                 n_retract_latest=None,
                 retraction_reason=None,
                 detector_status=None,
                 is_pre_sn=False,
                 firedrill_mode=True,
                 **kwargs):
        """
        Parameters
        ----------
        env_file: `str`
            path to env file, defaults to None
        detector_name: `str`
            Name of your detector,defaults to None.
            See auxiliary/detector_properties.json for available detector names.
        machine_time: `str`
            time recorded by your detector, defaults to None
            format: '%y/%m/%d %H:%M:%S:%f'
        neutrino_time: `str`
            time stamp of initial neutrino signal, defaults to None
            format: '%y/%m/%d %H:%M:%S:%f'
        p_val: `float`
            p value of possible neutrino observation(s), defaults to None
        p_values: `list`
            p values of possible neutrino observation(s),defaults to None.
            list of floats
        t_bin_width: `float`
            width of time window [sec] ,defaults to None.
        timing_series: `list`
            defaults to None
            list of strings, format: '%y/%m/%d %H:%M:%S:%f'
        which_tier: `str`
            which tier are you trying to retract from, defaults to None.
            Options:
                'CoincidenceTier'
                'SigTier'
                'TimingTier'
                'ALL'
        n_retract_latest: `int`
            how many of your last messages do you want to retract, defaults to None
        retraction_reason: `str`
            (optional) share with SNEWS what caused your false observation, defaults to None.
            We won't judge you :)
        detector_status: `str`
            tell SNEWS if your detector is ON or OFF, defaults to None.
            Options:
                'ON'
                'OFF'
        is_pre_sn: `bool`
            Set to True if your detector saw a pre-SN event, defaults to False.
        firedrill_mode : `bool`
                tell Publisher to send messages to the firedrill hop broker, defaults to True
        kwargs:
            extra stuff you want to send to SNEWS
        """
        if detector_name == "TEST":
            detector_name = snews_pt_utils.get_name()
        self.message_data = {'detector_name': detector_name,
                             'machine_time': machine_time,
                             'neutrino_time': neutrino_time,
                             'p_val': p_val,
                             'p_values': p_values,
                             't_bin_width': t_bin_width,
                             'timing_series': timing_series,
                             'which_tier': which_tier,
                             'n_retract_latest': n_retract_latest,
                             'retraction_reason': retraction_reason,
                             'detector_status': detector_status,
                             'is_pre_sn': is_pre_sn, }
        self.meta = dict(**kwargs)
        # self.message_data['meta'] = self.meta   # this is already done in tier decider
        self.message_data = {**self.message_data, ** self.meta}
        self.env_file = env_file
        stamp_time = datetime.utcnow().isoformat()
        self.messages, self.tiernames = snews_pt_utils._tier_decider(self.message_data, sent_time=stamp_time, env_file=env_file)
        self.firedrill_mode = firedrill_mode
    @classmethod
    def from_json(cls, jsonfile, env_file=None, **kwargs):
        """ Read the data from a json file
            Additional data / overwrite is allowed

        """
        input_json = snews_pt_utils._parse_file(jsonfile)
        output_data = {**input_json, **kwargs}
        return cls(env_file=env_file, **output_data)

    def send_to_snews(self, auth=True, verbose=True):
        """ Send the message to SNEWS
            Parameters
            ----------
            verbose : `bool`
                Whether to display the sent message
            auth : `bool`
                whether to authenticate with hop

        """
        with Publisher(env_path=self.env_file, verbose=verbose,  auth=auth, firedrill_mode=self.firedrill_mode) as pub:
            pub.send(self.messages)
