"""Test publishing timesificane tier messages."""
from SNEWS_PT.snews_pub import SNEWSTiersPublisher

def test_timesificance_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    tims = SNEWSTiersPublisher(detector_name='XENONnT', time_series=['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910'], p_values=[0.4, 0.5])

    # Check that message has expected structure.
    assert times.tiernames == ['CoincidenceTier', 'TimeTier']
    assert times.args_dict == {'detector_name': 'XENONnT', 'neutrino_time': '12/06/09 15:31:08:1098', 'timing_series': ['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910'], 'is_pre_sn': False}
    assert times.messages == [{'_id': '19_CoincidenceTier_None', 'detector_name': 'XENONnT', 'machine_time': None, 'schema_version': '1.0.1', 'neutrino_time': '12/06/09 15:31:08:1098', 'p_val': None, 'meta': {}}, {'_id': '19_TimeTier_None', 'detector_name': 'XENONnT', 'machine_time': None, 'schema_version': '1.0.1', 'neutrino_time': '12/06/09 15:31:08:1098', 'timing_series': ['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910'], 'meta': {}}]
    assert times.env_file == None

    # Try to send message to SNEWS 2.0 server.
    try:
        times.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
