# # -*- coding: utf-8 -*-
# """Unit tests for the snews_pt.pub
# """
#
# import unittest
# from hop import Stream
### THESE ======> CoincidenceTier, SignificanceTier, TimingTier NO LONGER EXISTS
# from SNEWS_PT.snews_pub import Publisher, CoincidenceTier, SignificanceTier, TimingTier
#
#
# class TestPubSub(unittest.TestCase):
#     def setUp(self):
#         self.obs_broker = "kafka://kafka.scimma.org/snews.experiments-test"
#         #  self.obs_broker = "kafka://hostname:port/gcn"
#         self.test_detector = 'TEST'
#         self.test_time = '00/00/00_00:00:00:1234'
#         self.test_timing_series = ['test', 'test']
#         self.test_p_val = 0.0
#         self.test_p_vals = [0.0, 0.0]
#         self.keys = ['_id', 'detector_name', 'sent_time', 'machine_time', 'neutrino_time', 'p_value', 'meta']
#
#     def tearDown(self):
#         print('Tearing down')
#         pass
#
#     def pub_test_coincidence(self):
#         with Publisher(verbose=False, auth=True, firedrill_mode=False) as pub:
#             message = CoincidenceTier(detector_name=self.test_detector, neutrino_time=self.test_time,
#                                       p_value=self.test_p_val, machine_time=self.test_time).message()
#             pub.send(message)
#
#     def test_pub_and_sub_coincidence(self):
#         stream = Stream(until_eos=True, auth=True)
#         with stream.open(self.obs_broker, 'r') as s:
#             self.pub_test_coincidence()
#             for message in s:
#                 test_message = message
#                 print('testing initial params')
#                 self.assertTrue(type(test_message) is dict)
#                 self.assertEqual(list(test_message.keys()), self.keys)
#                 self.assertEqual(message['detector_name'], self.test_detector)
#                 self.assertEqual(message['p_value'], self.test_p_val)
#                 self.assertEqual(message['neutrino_time'],self.test_time)
#                 break
#         pass
#
#
# if __name__ == '__main__':
#     unittest.main()
