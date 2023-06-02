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


class SNEWSMessage(ABC):
    """SNEWS 2.0 message interface. Defines base fields common to all messages and performs validation on messages during construction.

    Base fields:
    - id: string ID for the message (defined automatically for user).
    - schema_version: message schema version (defined automatically for user).
    - detector_name: name of detector (string), defined in snews_pt setup.
    """
    # Fields used in every message.
    basefields = [ '_id', 'schema_version', 'detector_name' ]

    def __init__(self, fields, detector_name='TEST', machine_time=None, **kwargs):
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
        det = self.get_detector_name(detector_name)
        mt = self.clean_time_input(machine_time)

        # Store basic message ID, detector name, and schema in a dictionary.
        self.message_data = dict(
            _id = f'{det}_{tier}_{mt}',
            schema_version = __version__,
            detector_name = det
            )

        for kw in kwargs:
            if kw in fields:
                # Append all kwargs matching subclass fields in message_data.
                self.message_data[kw] = kwargs[kw]
            else:
                # Append all non-matching kwargs to meta.
                self.meta[kw] = kwargs[kw]

        # Check that required fields are present and valid.
        self.validate()

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
        if detector_name == 'TEST' or detector_name == None:
            detector_name = snews_pt_utils.get_name()
        return detector_name

    def clean_time_input(self, time):
        """Get cleaned time string from input.

        Parameters
        ----------
        time : datetime or str
            Input time.

        Returns
        -------
        tmfmt : str
            Time string in ISO format.
        """
        if time is None:
            time = datetime.utcnow()

        if isinstance(time, str):
            time = fromisoformat(time)

        return time.isoformat()

    def validate(self):
        """Check for any missing required fields in the message constructed.
        """
        missing = []
        for f in self.reqfields:
            if f in self.message_data:
                if self.message_data[f] is None:
                    missing.append(f)
            else:
                missing.append(f)

        if missing:
            raise RuntimeError(f'{self.__class__.__name__} missing ' \
                               f'required field(s): {", ".join(missing)}.')

#    @classmethod
#    def from_json(cls, jsonfile, **kwargs):
#        with open(jsonfile, 'r') as infile:
#            jdata = json.load(infile)
#            return cls(*jdata, **kwargs) 
#
#    def to_json(self, jsonfile):
#        with open(jsonfile, 'w') as outfile:
#            json.dump(self.message_data, outfile, indent=4)


class SNEWSCoincidenceTierMessage(SNEWSMessage):
    """Message for SNEWS 2.0 coincidence tier."""

    reqfields = [ 'neutrino_time' ]

    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time',
                                                     'p_val' ] 

    def __init__(self, neutrino_time=None, p_val=None, **kwargs):
        super().__init__(self.fields,
            neutrino_time=self.clean_time_input(neutrino_time),
            p_val=p_val,
            **kwargs)


class SNEWSSignificanceTierMessage(SNEWSMessage):
    """Message for SNEWS 2.0 significance tier."""

    reqfields = [ 'p_values',
                  't_bin_width' ]

    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time' ]

    def __init__(self, p_values=None, t_bin_width=None, **kwargs):
        # Type check for proper types.
        if np.isscalar(p_values):
            raise RuntimeError(f'{self.__class__.__name__} p_values must be a list.')

        super().__init__(self.fields,
            p_values=p_values,
            t_bin_width=t_bin_width,
            **kwargs)


class SNEWSTimingTierMessage(SNEWSMessage):
    """Message for SNEWS 2.0 timing tier."""

    reqfields = [ 'timing_series' ]

    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time',
                                                     'neutrino_time',
                                                     'p_val' ]

    def __init__(self, neutrino_time=None, p_val=None, timing_series=None, **kwargs):
        super().__init__(self.fields,
            neutrino_time=self.clean_time_input(neutrino_time),
            p_val=p_val,
            timing_series=timing_series,
            **kwargs)


class SNEWSRetractionMessage(SNEWSMessage):
    """Message for SNEWS 2.0 retractions."""

    reqfields = [ 'retract_latest' ]

    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time',
                                                     'retraction_reason' ]

    def __init__(self, retract_latest=None, retraction_reason=None, **kwargs):
        super().__init__(self.fields,
            retract_latest=retract_latest,
            retraction_reason=retraction_reason,
            **kwargs)


class SNEWSHeartbeatMessage(SNEWSMessage):
    """Message for SNEWS 2.0 heartbeats."""

    reqfields = [ 'detector_status' ]

    fields = SNEWSMessage.basefields + reqfields + [ 'machine_time' ]

    def __init__(self, machine_time=None, detector_status=None, **kwargs):
        super().__init__(self.fields,
            machine_time=machine_time,
            detector_status=detector_status,
            **kwargs)


if __name__ == '__main__':
    try:
        sn = SNEWSCoincidenceTierMessage(neutrino_time=datetime.utcnow(), dude=5)
        print(SNEWSCoincidenceTierMessage.fields)
        print(f'{sn.message_data}\n\n')

        sn = SNEWSSignificanceTierMessage(p_values=[1], t_bin_width=1)
        print(SNEWSSignificanceTierMessage.fields)
        print(f'{sn.message_data}\n\n')

        sn = SNEWSTimingTierMessage(timing_series=[1,2,3])
        print(SNEWSTimingTierMessage.fields)
        print(f'{sn.message_data}\n\n')

        sn = SNEWSRetractionMessage(retract_latest=1)
        print(SNEWSRetractionMessage.fields)
        print(f'{sn.message_data}\n\n')

        sn = SNEWSHeartbeatMessage(detector_status='ON')
        print(SNEWSHeartbeatMessage.fields)
        print(f'{sn.message_data}')
    except RuntimeError as e:
        print(e)
