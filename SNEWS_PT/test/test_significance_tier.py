"""Test publishing significane tier messages."""
from SNEWS_PT.snews_pub import SNEWSTiersPublisher

def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSTiersPublisher(detector_name='DS-20K', neutrino_times=['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910'], p_values=[0.4, 0.5])

    # Check that message has expected structure.
    assert sign.tiernames == ['SigTier']
    assert sign.args_dict == {'detector_name': 'DS-20K', 'neutrino_times': ['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910'], 'p_values': [0.4, 0.5], 'is_pre_sn': False}
    assert sign.messages == [{'_id': '18_SigTier_None', 'detector_name': 'DS-20K', 'machine_time': None, 'schema_version': '1.0.1', 'neutrino_time': None, 'p_values': [0.4, 0.5], 'meta': {'neutrino_times': ['12/06/09 15:31:08:1098', '12/06/09 15:33:07:8910']}}]
    assert sign.env_file == None

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
    
