from .snews_pt_utils import TimeStuff, get_detector
from ._version import version as __version__


class Message_Schema:
    """ The Message scheme for the alert and observations

    Parameters
    ----------
    env_path : `str`, optional
        The path containing the environment configuration file
        If None, uses the default file in '/auxiliary/test-config.env'
    detector_key : `str`, optional
        The name of the detector. If None, uses "TEST"
    alert : `bool`, optional
        True if the message is ALERT message. Default is False.

    """

    def __init__(self, env_path=None, detector_key='TEST', is_pre_sn=False):
        self.times = TimeStuff(env_path)
        self.detector = get_detector(detector_key)
        self.detector_name = self.detector.name
        self.is_pre_sn = is_pre_sn

    def id_format(self, tier, machine_time):
        """ Returns formatted message ID
            time format should always be same for all detectors.
            The heartbeats and observation messages have the 
            same id format.

        Parameters
        ----------
        topic_state : `str`
            Can either be 'OBS', or  'ALERT'
        tier : `str`
            type of the message to be published. Can be;
            'TimeTier', 'SigTier', 'CoincidenceTier' for
            observation messages and, 'HeartBeat' for 
            heartbeat messages, and 'FalseOBS' for false
            observations.
        is_pre_sn : 'bool'
            Tell SNEWS whether signal is pre supernova
        time_received :

        Returns
            :`str`
                The formatted id as a string

        """
        if self.is_pre_sn:
            return f'{self.detector.id}_PRE-SN_{tier}_{machine_time}'
        else:
            return f'{self.detector.id}_{tier}_{machine_time}'

    def get_schema(self, tier, data, version=__version__):
        """ Create a message schema for given topic type.
            Internally called in hop_pub

            Parameters
            ----------
            tier : `str`
                type of the message to be published. Can be;
                'TimeTier', 'SigTier', 'CoincidenceTier' for
                observation messages and, 'HeartBeat' for
                heartbeat messages
            data      : dict
                dict object that contains message information.


            Returns
            -------
               :`dict`
                message with the correct scheme 

        """
        message = {"_id": self.id_format(tier=tier, machine_time=data['machine_time']),
                   "detector_name": self.detector_name,
                   "machine_time": data['machine_time'],
                   "schema_version": version
                   }
        if tier == 'Heartbeat':
            message['detector_status'] = data['detector_status']

        if tier == 'TimeTier':
            message['neutrino_time'] = data['neutrino_time']
            message['timing_series'] = data['timing_series']
            message['meta'] = data['meta']

        if tier == 'SigTier':
            message['neutrino_time'] = data['neutrino_time']
            message['p_values'] = data['p_values']
            message['meta'] = data['meta']

        if tier == 'CoincidenceTier':
            message['neutrino_time'] = data['neutrino_time']
            message['p_value'] = data['p_value']
            message['meta'] = data['meta']

        if tier == 'Retraction':
            message['which_tier'] = data['which_tier']
            message['N_retract_latest'] = data['N_retract_latest']
            message['retraction_reason'] = data['retraction_reason']

        if len(data.keys()) > len(message.keys()):
            for key in data.keys():
                if key not in message.keys():
                    message['_extra_' + key] = data[key]

        return message
