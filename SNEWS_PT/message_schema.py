
from .snews_pt_utils import TimeStuff, get_detector

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

    def __init__(self, env_path=None, detector_key='TEST'):
        self.times = TimeStuff(env_path)
        self.detector = get_detector(detector_key)
        self.detector_name = self.detector.name

    def id_format(self, topic_type):
        """ Returns formatted message ID
            time format should always be same for all detectors.
            The heartbeats and observation messages have the 
            same id format.

        Parameters
        ----------
        topic_state : `str`
            Can either be 'OBS', or  'ALERT'
        topic_type : `str`
            type of the message to be published. Can be;
            'TimeTier', 'SigTier', 'CoincidenceTier' for
            observation messages and, 'HeartBeat' for 
            heartbeat messages, and 'FalseOBS' for false
            observations.

        Returns
            :`str`
                The formatted id as a string

        """
        date_time = self.times.get_snews_time(fmt="%y/%m/%d_%H:%M:%S:%f")

        return f'{self.detector.id}_{topic_type}_{date_time}'

    def get_schema(self, message_type, data, sent_time):
        """ Create a message schema for given topic type.
            Internally called in hop_pub

            Parameters
            ----------
            message_type : `str`
                type of the message to be published. Can be;
                'TimeTier', 'SigTier', 'CoincidenceTier' for
                observation messages and, 'HeartBeat' for
                heartbeat messages
            data      : dict
                dict object that contains message information.
            sent_time : `str`
                time as a string

            Returns
            -------
               :`dict`
                message with the correct scheme 

        """
        message = {"_id": self.id_format(topic_type=message_type),
                   "detector_name": self.detector_name,
                   "sent_time": sent_time,
                   "machine_time": data['machine_time'],
                   }
        if message_type == 'Heartbeat':
            message['detector_status'] = data['detector_status']

        if message_type == 'TimeTier':
            message['neutrino_time'] = data['neutrino_time']
            message['timing_series'] = data['timing_series']
            message['meta'] = data['meta']

        if message_type == 'SigTier':
            message['neutrino_time'] = data['neutrino_time']
            message['p_values'] = data['p_values']
            message['meta'] = data['meta']

        if message_type == 'CoincidenceTier':
            message['neutrino_time'] = data['neutrino_time']
            message['p_value'] = data['p_value']
            message['meta'] = data['meta']

        if message_type == 'FalseOBS':
            message['false_id'] = data['false_id']
            message['which_tier'] = data['which_tier']
            message['N_retract_latest'] = data['N_retract_latest']
            message['which_tier'] = data['which_tier']
            message['retraction_reason'] = data['retraction_reason']

        if len(data.keys()) > len(message.keys()):
            for key in data.keys():
                if key not in message.keys():
                    message['_extra_' + key] = data[key]

        return message
