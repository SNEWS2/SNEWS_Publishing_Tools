
"""
The script to parse input data and decide on intended Tier(s)

"""
from inspect import signature
from .snews_pt_utils import set_env
from .snews_pt_utils import coincidence_tier_data, sig_tier_data, time_tier_data, heartbeat_data, retraction_data
from .message_schema import Message_Schema
from datetime import datetime
import os, sys

valid_keys = ["detector_name", "machine_time", "neutrino_time", "p_val", "p_values", "timing_series",
              "retract_latest", "retraction_reason", "detector_status", "is_pre_sn", 't_bin_width']

class TierDecider:
    def __init__(self, data, env_file=None):
        set_env(env_file)
        self.data = data
        self.meta_data = {}
        self.sent_time = datetime.utcnow().isoformat()
        self.schema = self.get_schema()
        self.decided_tiers = {}

    def decide(self):
        """ Decide how many messages need to be generated
            based on the contents.
        """
        # handle the meta data first
        self.handle_meta_fields()
        # CoincidenceTier if it has nu time
        if (type(self.data['neutrino_time']) == str) & ~(type(self.data['retract_latest']) == int):
            self.append_messages(coincidence_tier_data, 'CoincidenceTier')

        # SignificanceTier if it has p_values
        if type(self.data['p_values']) == list and type(self.data['t_bin_width']) == float:
            self.append_messages(sig_tier_data, 'SigTier')

        # TimingTier if timing_series exists
        if type(self.data['timing_series']) == list:
            self.append_messages(time_tier_data, 'TimeTier')

        # asking which tier doesn't make sense if the user doesn't know the tiers
        if type(self.data['retract_latest']) == int:
            self.append_messages(retraction_data, 'Retraction')

        # Heartbeat if there is detector status
        if type(self.data['detector_status']) == str:
            self.append_messages(heartbeat_data, 'Heartbeat')

        for t in self.decided_tiers.keys():
            print(f"Message Generated for {t}")

        if len(self.decided_tiers.keys())==0:
            print(f"No valid message is created! Check your input and try again!")
        # Return the names and messages generated
        return self.decided_tiers.values(), self.decided_tiers.keys()

    def get_schema(self):
        self.data["is_pre_sn"] = self.data.get("is_pre_sn", False)
        self.data['detector_name'] = self.data.get("detector_name", os.getenv('DETECTOR_NAME'))
        return Message_Schema(detector_key=self.data['detector_name'], is_pre_sn=self.data['is_pre_sn'])

    def handle_meta_fields(self):
        """ make a meta dict for all key-value pairs
            that don't belong any known keys
        """
        # if there are keys that wouldn't belong to any tier/command pass them as meta
        meta_keys = [key for key, value in self.data.items() if sys.getsizeof(value) < 2048]
        meta_data = {k: self.data[k] for k in meta_keys if k not in valid_keys}
        self.meta_data = meta_data

    def append_messages(self, tier_function, name):
        """ This function takes the relevant inputs and formats
        a message accordingly. The messages are collected in a list
        """
        tier_keys = list(signature(tier_function).parameters.keys())
        data_for_tier = {k: v for k, v in self.data.items() if k in tier_keys}
        data_for_tier = tier_function(**data_for_tier)
        if name not in ['Heartbeat']: # 'Retraction',
            # don't append meta field to Retraction and Heartbeat
            data_for_tier['meta'] = self.meta_data
        else:
            data_for_tier['meta'] = {}

        msg = self.schema.get_schema(tier=name, data=data_for_tier, sent_time=self.sent_time)

        self.decided_tiers[name] = msg
