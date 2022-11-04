


from datetime import datetime
import os, json
from .core.logging import getLogger, log_file
import warnings

log = getLogger(__name__)

# Check if detector name is in registered list.
detector_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'auxiliary/detector_properties.json'))
with open(detector_file) as file:
    snews_detectors = json.load(file)
snews_detectors = list(snews_detectors.keys())


class SnewsFormat:

    def __init__(self, message):
        self.message = message
        self.message_keys = message.keys()
        self.bypass = False # bypass if retraction, or remote command (bypasses all time checks!)
        self.is_test = self.check_if_test() # if True, don't check if times are reasonable (still checks format!)

    def __call__(self, *args, **kwargs):
        msg_as_json = json.dumps(self.message, sort_keys = True, indent = 4)
        test_str = " -TEST- " if self.is_test else " "
        log.debug("*"*40+f" LOGS FOR THE{test_str}MESSAGE\n"+ msg_as_json)
        valid = True
        try:
            assert self.check_id() is valid, "_id not valid" # if _id exists
            assert self.check_detector() is valid, "detector_name not valid" # if detector name is known
            assert self.check_message_type() is valid, "types not valid" # if valid type; check name and times
            assert self.check_times() is valid, "neutrino_time not valid" # if times are ISO format and reasonable
            assert self.check_pvals() is valid, "p_val not valid"# if exists, pvals are float and reasonable
            log.info("\t> All checks are passed. Message is in SnewsFormat.")
            log.debug("*" * 40 + " END OF lOGS\n")
            return valid
        except AssertionError as ae:
            log.error(f"\t> Following check failed: {ae}")
            warnings.warn(f"\n\n Following check failed: {ae} \nSee the full logs {log_file}", UserWarning)
            log.debug("*" * 40 + " END OF lOGS\n")
            return False
        except Exception as e:
            log.error(f"\t> Something went wrong! {e}")
            warnings.warn(f"\n\n Something went wrong! \nSee the full logs {log_file}", UserWarning)
            log.debug("*" * 40 + " END OF lOGS\n")
            return False

    def check_if_test(self):
        if "meta" in self.message_keys:
            if "is_test" in self.message['meta'].keys():
                return self.message["meta"]["is_test"]

    def check_id(self):
        """ check if the format is correct
            snews_pt sends messages in mongodb format
            which HAS TO contain an _id field
        """
        log.debug(f"\t> Checking _id ..")
        if "_id" not in self.message_keys:
            log.error(f"\t> Message without '_id' field")
            return False
        else:
            log.info(f"\t> Message has an '_id' field")
            idsplit = self.message['_id'].split('_')
            if len(idsplit) < 2:
                log.error(f"\t> Message '_id' has different format. Expected '#_string' got {self.message['_id']}")
                return False
            return True

    def check_detector(self):
        log.info(f"\t> Checking detector name.")
        if self.bypass:
            log.info(f"\t> Detector name check bypassed.")
            return True

        log.debug(f"\t> Checking detector name..")
        if 'detector_name' not in self.message_keys:
            log.error(f'\t> Does not have required key: "detector_name"')
            return False
        if self.message['detector_name'] not in snews_detectors:
            log.error(f'\t> Detector not found: {self.message["detector_name"]}')
            return False
        log.info(f'\t> Detector: {self.message["detector_name"]} valid')
        return True

    def check_message_type(self):
        """ We expect Tier messages, and Commands,
            and Tier messages require different checks
        """
        log.debug(f"\t> Checking message type..")
        if "hard-reset" in self.message['_id']:
            log.debug("\t> Hard reset. Skipping format check.")
            self.bypass = True

        elif "test-connection" in self.message['_id']:
            log.debug("\t> Test Connection. Skipping format check.")
            self.bypass = True

        elif 'Heartbeat' in self.message['_id']:
            log.debug("\t> Heartbeat Passed. Checking time and status.")
            if not self.check_detector_status(): # if detector_status does not exist, return False
                log.error("\t> Heartbeat not valid!")
                return False
            self.bypass = True

        elif "Retraction" in self.message['_id']:
            log.debug(f"\t> Retraction Passed.")
            self.bypass = True

        elif [i in self.message['_id'] for i in ['TimeTier', 'SigTier', 'CoincidenceTier']]:
            log.debug(f"\t> Tier message Passed. Checking times.")

        else:
            log.error(f"\t> Unknown id Passed : {self.message['_id']}.")
            return False
        log.info(f"\t> Message type : {self.message['_id']} valid.")
        return True

    def check_detector_status(self):
        """ if _id is for HB, check detector status field and neutrino time
        """
        log.debug(f"\t> Checking detector status..")
        if "detector_status" not in self.message_keys:
            log.error(f"\t> Heartbeat Message but detector_status not in keys.")
            return False
        if self.message["detector_status"].upper() not in ["ON", "OFF"]:
            log.error(f"\t> detector_status not ON or OFF.")
            return False
        log.info(f"\t> detector_status is valid.")
        return True

    def check_times(self):
        log.debug(f"\t> Checking Times..")
        if self.bypass:
            log.info(f"\t> Time checks bypassed.")
            return True

        # check if neutrino times exists and in string format
        if 'neutrino_time' not in self.message_keys:
            log.error(f"\t> neutrino_time does not exist!.")
            return False
        if type(self.message['neutrino_time']) is not str:
            log.error(f"\t> neutrino_time is not a string!.")
            return False
        log.info(f"\t> neutrino_time exists and is string.")

        # it exists and string, check if ISO format, and reasonable
        try:
            dateobj = datetime.fromisoformat(self.message["neutrino_time"])
            log.info(f"\t> neutrino_time is ISO formattable.")
        except Exception as e:
            log.error("\t> neutrino_time does not match "
                      f"SNEWS 2.0 (ISO) format: '%Y-%m-%dT%H:%M:%S.%f'\n\t{e}")
            return False

        # neutrino_times exists, and in str - ISO format, check dates
        if self.is_test:
            # for tests, exact time is irrelevant
            log.info(f"\t> neutrino_time is checked for is_test=True, not checking time interval.")
            return True

        if (dateobj - datetime.utcnow()).total_seconds() <= -172800.0:
            log.error(f'\t> neutrino time is more than 48 hrs olds !\n')
            return False

        if (dateobj - datetime.utcnow()).total_seconds() > 0:
            log.error(f'\t> neutrino time comes from the future, please stop breaking causality.')
            return False
        # if all passed, return True
        log.info(f"\t> neutrino_time passed all time checks.")
        return True

    def check_pvals(self):
        """ check if p_val exists, and valid
        """
        log.debug(f"\t> Checking p_val..")
        if 'p_val' in self.message_keys:
            if self.message['p_val'] is None:
                log.info(f"\t> p_val is deafulted to None.")
                return True # does not exist/default to None

            pval = self.message['p_val']
            pval_type = type(pval)

            if pval_type is not float:
                log.error(f'\t> p value needs to be a float type, type given: {pval_type}.')
                return False
            if pval >= 1.0 or pval <= 0:
                log.error(f'\t> {pval} is not a valid p value !')
                return False
            log.info(f"\t> p_val={pval} is valid!")
        log.info(f"\t> no p_val in message keys.")
        # still return True, it is not a must
        return True

