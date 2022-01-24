import unittest
from SNEWS_PT.snews_pub import Publisher, CoincidenceTier, SignificanceTier, TimingTier


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.test_detector = 'TEST'
        self.test_time = '00/00/00_00:00:00:1234'
        self.test_timing_series = ['00:00:00:1234', '00:00:00:1234']
        self.test_p_val = 0.0
        self.test_p_vals = [0.0, 0.0]
        self.coincidence_schema = {
            '_id': '',
            'detector_name': 'TEST',
            'sent_time': '',
            'machine_time': self.test_time,
            'neutrino_time': self.test_time,
            'p_value': self.test_p_val,
            'meta': {}
        }
        self.timing_series_schema = {
            '_id': '',
            'detector_name': 'TEST',
            'sent_time': '',
            'machine_time': self.test_time,
            'neutrino_time': self.test_time,
            'timing_series': self.test_timing_series,
            'meta': {}
        }
        self.significance_tier_schema = {
            '_id': '',
            'detector_name': 'TEST',
            'sent_time': '',
            'machine_time': self.test_time,
            'neutrino_time': self.test_time,
            'p_values': self.test_p_vals,
            'meta': {}
        }

    def tearDown(self):
        pass

    def test_coincidence_schema(self):
        """
        Test schema for coincidence

        """

        schema = CoincidenceTier(detector_name=self.test_detector, neutrino_time=self.test_time,
                                 machine_time=self.test_time, p_value=self.test_p_val).message()
        self.coincidence_schema['_id'] = schema['_id']
        self.coincidence_schema['sent_time'] = schema['sent_time']

        # test for type
        self.assertTrue(type(schema) is dict)
        # test content
        self.assertEqual(self.coincidence_schema, schema)
        self.assertEqual(list(self.coincidence_schema.keys()), list(schema.keys()))
        self.assertEqual(len(schema['_id'].split('_')), 4)

    def test_timing_schema(self):
        """
        Test schema for timing series

        """
        schema = TimingTier(detector_name=self.test_detector, neutrino_time=self.test_time,
                            machine_time=self.test_time, timing_series=self.test_timing_series).message()
        self.timing_series_schema['_id'] = schema['_id']
        self.timing_series_schema['sent_time'] = schema['sent_time']
        # test for type
        self.assertTrue(type(schema) is dict)
        self.assertEqual(self.timing_series_schema, schema)
        self.assertEqual(list(self.timing_series_schema.keys()), list(schema.keys()))
        self.assertEqual(len(schema['_id'].split('_')), 4)

    def test_significance_schema(self):
        """
        Test schema for significance
        """
        schema = SignificanceTier(detector_name=self.test_detector, neutrino_time=self.test_time,
                                  machine_time=self.test_time, p_values=self.test_p_vals).message()
        self.significance_tier_schema['_id'] = schema['_id']
        self.significance_tier_schema['sent_time'] = schema['sent_time']
        self.assertTrue(type(schema) is dict)
        self.assertEqual(self.significance_tier_schema, schema)
        self.assertEqual(list(self.significance_tier_schema.keys()), list(schema.keys()))
        self.assertEqual(len(schema['_id'].split('_')), 4)


if __name__ == '__main__':
    unittest.main()
