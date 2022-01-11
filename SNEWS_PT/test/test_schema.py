import unittest
from SNEWS_PT.snews_pub import Publisher, CoincidenceTier, SignificanceTier, TimingTier

class TestSchema(unittest.TestCase):
    def setUp(self):
        self.test_detector = 'TEST'
        self.test_time = '00/00/00_00:00:00:1234'
        self.test_timing_series = ['test', 'test']
        self.test_p_val = 0.0
        self.test_p_vals = [0.0, 0.0]
        self.coincidence_schema = {
            '_id': '',
            'detector_name': 'TEST',
            'sent_time': '',
            'machine_time': self.test_time,
            'neutrino_time': self.test_time,
            'p_value': self.test_p_val
        }

    def tearDown(self):
        pass

    def test_coincidence_schema(self):
        """
        Test coincidence publish

        """

        schema = CoincidenceTier(detector_name=self.test_detector, neutrino_time=self.test_time,
                                 machine_time=self.test_time, p_value=self.test_p_val).message()
        self.coincidence_schema['_id'] = schema['_id']
        self.coincidence_schema['sent_time'] = schema['sent_time']

        # test for type
        self.assertTrue(type(schema) is dict)
        # test content
        self.assertEqual(self.coincidence_schema, schema)

    def test_timing_schema(self):
        """
        Test coincidence publish

        """
        schema = TimingTier(detector_name=self.test_detector, neutrino_time=self.test_time,
                            machine_time=self.test_time, timing_series=self.test_timing_series).message()

        # test for type
        print(schema)
        self.assertTrue(type(schema) is dict)

if __name__ == '__main__':
    unittest.main()
