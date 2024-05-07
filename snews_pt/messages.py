"""Interface for SNEWS messages.
"""

import os
import click
import json
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
try:
    fromisoformat = datetime.fromisoformat
except AttributeError as e:
    from dateutil.parser import isoparse as fromisoformat

from hop import Stream
try:
    from hop.models import JSONBlob
except ImportError as e:
    raise ImportError(f'{e}\nSNEWS Publishing Tools and Coincidence System requires op version >= 0.8.0')

from snews_pt import snews_pt_utils
from snews_pt._version import version as __version__

class Publisher:

    def __init__(self, env_path=None, verbose=True, auth=True, firedrill_mode=True):
        """Class in charge of publishing messages to SNEWS-hop sever.
        This class acts as a context manager.

        Parameters
        ----------
        env_path: str
            path to SNEWS env file, defaults to tes_config.env if None is passed.
        verbose: bool
            Option to display message when publishing.
        auth: bool
            Option to run hop-Stream without authentication. Pass False to do so
        firedrill_mode :bool
            whether to use firedrill broker

        """
        snews_pt_utils.set_env(env_path)
        self.auth = auth
        self.verbose = verbose

        self.obs_broker = os.getenv("OBSERVATION_TOPIC")
        if firedrill_mode:
            self.obs_broker = os.getenv("FIREDRILL_OBSERVATION_TOPIC")


    def __enter__(self):
        self.stream = Stream(until_eos=True, auth=self.auth).open(self.obs_broker, 'w')
        return self

    def __exit__(self, *args):
        self.stream.close()

    def send(self, messages):
        """ This method will set the sent_time and send the message to the hop broker.

        Parameters
        ----------
        messages: `list`
            list containing observation message.

        """
        if len(messages) == 0:
            # None of the messages passed the format checker!
            raise UserWarning("No valid message exists!")

        if type(messages) == dict:
            messages = list(messages)
        for message in messages:
            message["sent_time"] = np.datetime_as_string(np.datetime64(datetime.utcnow().isoformat()), unit='ns')
            self.stream.write(JSONBlob(message))
            self.display_message(message)

    def display_message(self, message):
        if self.verbose:
            tier = message['_id'].split('_')[1]
            click.secho(f'{"-" * 64}', fg='bright_blue')
            click.secho(f'Sending message to {tier} on {self.obs_broker}', fg='bright_red')
            if tier == 'Retraction':
                click.secho("It's okay, we all make mistakes".upper(), fg='magenta')
            snews_pt_utils.prettyprint_dictionary(message)


def clean_time_input(input_datetime):
    """Get cleaned time string from input.

    Parameters
    ----------
    input_datetime : np.datetime64, datetime.datetime or str

    Returns
    -------
        Time string in ISO format.
    """
    if input_datetime is None:
        return np.datetime_as_string(np.datetime64(datetime.utcnow().isoformat()), unit='ns')

    if isinstance(input_datetime, (str, np.datetime64, datetime)):
        # If the input is already a string or NumPy datetime64, return it as is
        dt = np.datetime64(input_datetime)
        return np.datetime_as_string(dt, unit='ns')
    else:
        raise ValueError(
            f"Unsupported datetime type: {type(input_datetime)}. Supported types: str, np.datetime64, pd.Timestamp, datetime.datetime")


class SNEWSMessage(ABC):
    """SNEWS 2.0 message interface. Defines base fields common to all messages and performs validation on messages during construction.

    Base fields:
    - id: string ID for the message (defined automatically for user).
    - schema_version: message schema version (defined automatically for user).
    - detector_name: name of detector (string), defined in snews_pt setup.
    """
    # Fields used in every message.
    basefields = [ '_id', 'schema_version', 'detector_name' ]

    def __init__(self, fields, detector_name='TEST', **kwargs):
        """Build a generic abstract message object for SNEWS 2.0.

        Parameters
        ----------
        fields : list
            List of all fields expected in the message.
        detector_name : str
            Name of detector sending the message.
        machine_time : datetime or str
            Machine time.
        """
        self.meta =  {}

        # Set tier using the subclass name (CoincidenceTier, TimeTier, ...)
        tier = self.__class__.__name__.replace('SNEWS','').replace('Message','')

        # Get the detector name from the input.
        det = self.get_detector_name(detector_name) # just fetches from the env
        # det = snews_pt_utils.set_name(detector_name, _return=True) # rewrites the env each time
        raw_mt = kwargs.pop('machine_time', None)
        mt = clean_time_input(raw_mt)
        # raw_mt = mt if isinstance(raw_mt, str) else None

        # Store basic message ID, detector name, and schema in a dictionary.
        self.message_data = dict(
            _id = f'{det}_{tier}_{mt}',
            schema_version = __version__,
            detector_name = det,
            machine_time = mt
            )

        self.is_test = kwargs.get('is_test', False)
        for kw in kwargs:
            if kw in fields:
                # Append all kwargs matching subclass fields in message_data.
                self.message_data[kw] = kwargs[kw]
            else:
                # Append all non-matching kwargs to meta.
                self.meta[kw] = kwargs[kw]

        # Check that required fields are present and valid.
        self.has_required_fields()

    def print_schema(self):
        click.secho(f'Message schema for {self.__class__.__name__}', bg='white', fg='blue')
        for f in self.fields:
            if f in self.basefields:
                click.secho(f'{f:<20s} : (SET AUTOMATICALLY)', fg='bright_red')
            elif f in self.reqfields:
                click.secho(f'{f:<20s} : (REQUIRED USER INPUT)', fg='bright_blue')
            else:
                click.secho(f'{f:<20s} : (USER INPUT)', fg='bright_cyan')
        click.secho(f'{"**kwargs":<20s} : (GROUPED AS META)', fg='bright_green')

    def get_detector_name(self, detector_name):
        """Get formatted detector name.

        Parameters
        ----------
        detector_name : str or None
            Name of the detector.

        Returns
        -------
        detector_name : str
            Correctly formatted detector name.
        """
        if detector_name == 'TEST' or detector_name is None:
            detector_name = snews_pt_utils.get_name()
        else:
            detector_name = snews_pt_utils.set_name(detector_name, _return=True)
        return detector_name

    def has_required_fields(self):
        """Validate the message on construction.
        """
        missing = []
        for f in self.reqfields:
            if f in self.message_data:
                if self.message_data[f] is None:
                    missing.append(f)
            else:
                missing.append(f)

        if missing:
            raise RuntimeError(f'{self.__class__.__name__} missing '
                               f'required field(s): {", ".join(missing)}.')

    def __repr__(self):
        _repr_str = click.style(f'{self.__class__.__name__}\n', bold=True)
        _repr_str += f'{"-"*len(self.__class__.__name__)}\n'
        for k, v in self.message_data.items():
            if k in self.basefields:
                _repr_str += click.style(f"{k:>15} : {v}\n", fg='bright_red')
            elif k in self.fields and k not in self.basefields and k not in self.reqfields:
                _repr_str += click.style(f"{k:>15} : {v}\n", fg='black')
            elif k in self.reqfields:
                _repr_str += click.style(f"{k:>15} : {v}\n", fg='bright_blue', bold=True)
        # _repr_str += f'{"-"*len(self.__class__.__name__)}\n'
        for k, v in self.meta.items():
            _repr_str += click.style(f"{k:>15} : {v}\n", fg='bright_cyan')
        return _repr_str

    def __repr_markdown__(self):
        _repr_str = f'### {self.__class__.__name__}\n'
        for k, v in self.message_data.items():
            _repr_str += f"**{k}** : {v}\n"
        _repr_str += f'---\n'
        for k, v in self.meta.items():
            _repr_str += f"**{k}** : {v}\n"
        return _repr_str

    @abstractmethod
    def is_valid(self):
        """Check that parameter values are valid for this tier."""
        pass

    def to_json(self, jsonfile):
        with open(jsonfile, 'w') as outfile:
            json.dump(self.message_data, outfile, indent=4)


class SNEWSCoincidenceTierMessage(SNEWSMessage):
    """Message for SNEWS 2.0 coincidence tier."""

    reqfields = [ 'neutrino_time' ]
    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time', 'p_val', 'is_test' ]

    def __init__(self, neutrino_time=None, p_val=None, **kwargs):
        super().__init__(self.fields,
                         neutrino_time=clean_time_input(neutrino_time),
                         p_val=p_val,
                         **kwargs)

    def is_valid(self):
        """Check that parameter values are valid for this tier.
            Detector name must be known, neutrino times must make sense, etc. if not test"""
        if not self.is_test:
            # time format is corrected at the base class, check if reasonable
            dateobj = np.datetime64(self.message_data['neutrino_time'])
            duration = (dateobj - np.datetime64(datetime.utcnow()))/np.timedelta64(1, 's')
            if (duration <= -172800.0) or (duration > 0.0):
                raise ValueError(f'{self.__class__.__name__} neutrino_time must be within 48 hours of now.')

            # p_val must be a float between 0 and 1
            pv = self.message_data['p_val']
            if isinstance(pv, str):
                pv = float(pv)
            if not (0.0 <= pv <= 1.0):
                raise ValueError(f'{self.__class__.__name__} p_value of the detection must be between 0 and 1.')

        return True


class SNEWSSignificanceTierMessage(SNEWSMessage):
    """Message for SNEWS 2.0 significance tier."""

    reqfields = [ 'p_values', 't_bin_width' ]
    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time', 'is_test' ]

    def __init__(self, p_values=None, t_bin_width=None, **kwargs):
        super().__init__(self.fields,
                         p_values=p_values,
                         t_bin_width=t_bin_width,
                         **kwargs)

    def is_valid(self):
        """Check that parameter values are valid for this tier."""
        if not self.is_test:
            # Type check for proper types.
            if np.isscalar(self.message_data['p_values']):
                raise RuntimeError(f'{self.__class__.__name__} p_values must be a list.')
            for pv in self.message_data['p_values']:
                if isinstance(pv, str):
                    pv = float(pv)
                if not (0.0 <= pv <= 1.0):
                    raise ValueError(f'{self.__class__.__name__} p_values must be between 0 and 1.')
            if isinstance(self.message_data['t_bin_width'], str):
                if not self.message_data['t_bin_width'].replace('.','',1).isdigit():
                    raise ValueError(f'{self.__class__.__name__} t_bin_width must be a float.')
            elif not isinstance(self.message_data['t_bin_width'], float):
                raise ValueError(f'{self.__class__.__name__} t_bin_width must be a float.')

        return True


class SNEWSTimingTierMessage(SNEWSMessage):
    """ Message for SNEWS 2.0 timing tier.
        `timing_series` can either be list of string or nanosecond-precision integers
        representing the time after the initial neutrino time.
    """

    reqfields = [ 'timing_series', 'neutrino_time' ]
    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time', 'p_val', 'is_test' ]

    def __init__(self, p_val=None, timing_series=None, neutrino_time=None, **kwargs):
        initial_nu_time_str = clean_time_input(neutrino_time)
        initial_nu_time_object = np.datetime64(initial_nu_time_str).astype('datetime64[ns]')
        # first convert the timing series into relative times
        times = self._convert_times(timing_series, initial_neutrino_time=initial_nu_time_object)
        super().__init__(self.fields,
                         p_val=p_val,
                         timing_series=times,
                         neutrino_time=initial_nu_time_str,
                         **kwargs)

    def _convert_times(self, timing_series, initial_neutrino_time):
        if all([isinstance(t, str) for t in timing_series]):
            # convert to numpy datetime objects
            times_obj = np.array([np.datetime64(t) for t in timing_series]).astype('datetime64[ns]')
            times_obj = np.sort(times_obj)
            initial_neutrino_time = times_obj[0] if initial_neutrino_time is None else initial_neutrino_time
            # make sure they are always ns precision
            relative_times = (times_obj - initial_neutrino_time).astype('timedelta64[ns]').astype(int).tolist()
        elif all([isinstance(t, (int, float)) for t in timing_series]):
            # then we assume they are relative times from the first neutrino time with ns precision
            relative_times = timing_series if isinstance(timing_series, list) else list(timing_series)
        else:
            raise ValueError(f'{self.__class__.__name__} timing_series must be a list of isoformat strings or '
                             f'ns-precision floats from the first neutrino time.')
        return relative_times


    def is_valid(self):
        """Check that parameter values are valid for this tier.
            timing series can either be a list of iso-convertible strings or a list of floats."""

        if not self.is_test:
            # Check timing validity
            # expect to see a monotonic increase in the relative times
            is_monotonic = np.all(np.diff(self.message_data['timing_series']) >= 0)
            if not is_monotonic:
                raise ValueError(f'{self.__class__.__name__} timing_series must be in increasing order. '
                                 f'They represent the time after initial neutrino time')

            # p_val must be a float between 0 and 1
            pv = self.message_data['p_val']
            if isinstance(pv, str):
                pv = float(pv)
            if not (0.0 <= pv <= 1.0):
                raise ValueError(f'{self.__class__.__name__} p_value of the detection must be between 0 and 1.')
        return True


class SNEWSRetractionMessage(SNEWSMessage):
    """Message for SNEWS 2.0 retractions."""

    reqfields = [ 'retract_latest' ]
    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time', 'retraction_reason', 'is_test' ]

    def __init__(self, retract_latest=None, retraction_reason=None, **kwargs):
        super().__init__(self.fields,
                         retract_latest=retract_latest,
                         retraction_reason=retraction_reason,
                         **kwargs)

    def is_valid(self):
        """Check that parameter values are valid for this tier."""
        if not isinstance(self.message_data['retract_latest'], int):
            raise ValueError(f'{self.__class__.__name__} retract_latest must be a positive integer.')
        return True


class SNEWSHeartbeatMessage(SNEWSMessage):
    """Message for SNEWS 2.0 heartbeats."""

    reqfields = [ 'detector_status' ]
    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time', 'is_test' ]

    def __init__(self, machine_time=None, detector_status=None, **kwargs):
        super().__init__(self.fields,
                         machine_time=machine_time,
                         detector_status=detector_status,
                         **kwargs)

    def is_valid(self):
        """Check that parameter values are valid for this tier."""
        status = self.message_data['detector_status']
        if not isinstance(status, str) or status not in ['ON', 'OFF']:
            raise ValueError(f'{self.__class__.__name__} detector_status must be either "ON" or "OFF".')
        return True


class SNEWSMessageBuilder:
    """Builder class that takes a list of message fields and builds all
    appropriate messages for SNEWS 2.0 tiers based on the child classes of
    SNEWSMessage. The class contains a messages' parameter that stores the list
    of SNEWSMessage child instances.
    """

    def __init__(self, env_file=None,
                 detector_name='TEST',
                 machine_time=None,
                 neutrino_time=None,
                 p_val=None,
                 p_values=None,
                 t_bin_width=None,
                 timing_series=None,
                 retract_latest=None,
                 retraction_reason=None,
                 detector_status=None,
                 is_test=False,
                 **kwargs):

        self.messages = None
        self.selected_tiers = []

        self._build_messages(env_file=env_file,
                             detector_name=detector_name,
                             machine_time=machine_time,
                             neutrino_time=neutrino_time,
                             p_val=p_val,
                             p_values=p_values,
                             t_bin_width=t_bin_width,
                             timing_series=timing_series,
                             retract_latest=retract_latest,
                             retraction_reason=retraction_reason,
                             detector_status=detector_status,
                             is_test=is_test,
                             **kwargs)

    def __repr__(self):
        _repr_str = f'{self.__class__.__name__}:\n'
        if self.messages is None:
            _repr_str += 'No messages have been built.'
        else:
            for m in self.messages:
                _repr_str += f'{m.__class__.__name__}:\n'
                for k, v in m.message_data.items():
                    _repr_str += f"  **{k}** : {v}\n"
                _repr_str += f'---\n'
                for k, v in m.meta.items():
                    _repr_str += f"  **{k}** : {v}\n"
        return _repr_str

    def __repr_markdown__(self):
        _repr_str = click.style(f'{self.__class__.__name__}:\n', bold=True)
        if self.messages is None:
            _repr_str += 'No messages have been built.'
        else:
            for m in self.messages:
                _repr_str += m.__repr_markdown__()
                _repr_str += 30*'-'+'\n'
        return _repr_str

    def _build_messages(self, **kwargs):
        """Utility function to create messages for all appropriate tiers.
        """
        # Initialize the message list.
        self.messages = None

        # Identify all non-null keyword arguments passed to the class constructor.
        nonull_keys = [k for k in kwargs if kwargs[k] is not None]
        nonull_kwargs = {k: kwargs[k] for k in nonull_keys}

        # Loop through all message types.
        # To do: create a message type registry in this module?
        for smc in [SNEWSCoincidenceTierMessage,
                    SNEWSSignificanceTierMessage,
                    SNEWSTimingTierMessage,
                    SNEWSRetractionMessage,
                    SNEWSHeartbeatMessage]:

            # If the required fields for a given message tier are present
            # in this class, create a list of message objects.
            hasreqfields = all(_ in nonull_keys for _ in smc.reqfields)
            if hasreqfields:
                if self.messages is None:
                    # check is valid at creation
                    smc(**nonull_kwargs).is_valid()
                    self.messages = [smc(**nonull_kwargs)]
                else:
                    self.messages.append(smc(**nonull_kwargs))
                self.selected_tiers.append(smc.__name__)

    @classmethod
    def from_json(cls, jsonfile, **kwargs):
        """Build SNEWSMessage instances using a message in JSON format.

        Parameters
        ----------
        jsonfile : str
            Name of JSON file.
        """
        with open(jsonfile, 'r') as infile:
            jdata = json.load(infile)
        return cls(**jdata, **kwargs)

    def send_messages(self, firedrill_mode=True, env_file=None, verbose=True, auth=True):
        """Send all messages in the messages list to the SNEWS server.
            Merges the meta fields accordingly before sending."""
        # all req fields
        fields_set = set({k: v for m in self.messages for k, v in m.message_data.items()})
        messages_to_send = []

        # append meta fields if the meta field is not in the other messages
        meta_dict = {}
        for m in self.messages:
            mes = m.message_data
            met = m.meta
            for k, v in met.items():
                # store meta fields to append later
                # if the meta field is not in the other messages
                if k not in fields_set:
                    meta_dict[k] = v
            mes["meta"] = meta_dict
            messages_to_send.append(mes)

        with Publisher(env_path=env_file,
                       verbose=verbose,
                       auth=auth,
                       firedrill_mode=firedrill_mode) as pub:
            pub.send(messages_to_send)


if __name__ == '__main__':
    try:
        # Build the individual message classes.
        sn = SNEWSCoincidenceTierMessage(neutrino_time=datetime.utcnow(), dude=5)
        sn.print_schema()
        print(f'{sn.message_data}\n\n')

        sn = SNEWSSignificanceTierMessage(p_values=[1], t_bin_width=1)
        sn.print_schema()
        print(f'{sn.message_data}\n\n')

        sn = SNEWSTimingTierMessage(timing_series=[1,2,3])
        sn.print_schema()
        print(f'{sn.message_data}\n\n')

        sn = SNEWSRetractionMessage(retract_latest=1)
        sn.print_schema()
        print(f'{sn.message_data}\n\n')

        sn = SNEWSHeartbeatMessage(detector_status='ON')
        sn.print_schema()
        print(f'{sn.message_data}\n\n')

        # Use the builder class.
        print('Exercise the SNEWSMessageBuilder:\n')
        sm = SNEWSMessageBuilder(
                neutrino_time=datetime.utcnow(),
                p_values=[1],
                t_bin_width=1,
                timing_series=[1,2,3]
                )

        # Print generated messages in the SNEWSMessageBuilder, save to JSON.
        print('Messages created and saved to JSON:')
        for j, msg in enumerate(sm.messages):
            jsonfile = f'{msg.__class__.__name__}.json'
            print(j, msg.__class__.__name__, msg.message_data)
            msg.to_json(jsonfile)

        # Instantiate messages from JSON.
        from glob import glob
        jsonfiles = sorted(glob('*.json'))
        for jsonfile in jsonfiles:
            print(f'\nMessages from JSON file {jsonfile}:\n')
            sm.from_json(jsonfile)
            for j, msg in enumerate(sm.messages):
                jsonfile = f'{msg.__class__.__name__}.json'
                print(j, msg.__class__.__name__, msg.message_data, '\n')

    except RuntimeError as e:
        print(e)
