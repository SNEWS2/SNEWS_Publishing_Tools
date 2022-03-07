"""Test publishing coincidence tier messages."""
from SNEWS_PT.snews_pub import SNEWSTiersPublisher

def test_coincidence_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='12/06/09 15:31:08:1098', p_value=0.4)
    # Check that message has expected structure.
    assert coin.tiernames == ['CoincidenceTier']
    assert coin.message_data == {'detector_name': 'KamLAND', 'machine_time': None, 'neutrino_time': '12/06/09 15:31:08:1098', 
                                 'p_val': None, 'p_values': None, 'timing_series': None, 'which_tier': None, 'n_retract_latest': None, 
                                 'retraction_reason': None, 'detector_status': None, 'is_pre_sn': False, 't_bin_width': None, 'meta': {'p_value': 0.4}}
    assert coin.messages == [{'_id': '4_CoincidenceTier_None', 'detector_name': 'KamLAND', 'machine_time': None, 'neutrino_time': '12/06/09 15:31:08:1098', 
                              'p_val': None, 'meta': {'meta': {'p_value': 0.4}}, 'schema_version': '1.1.0'}]
    assert coin.env_file == None
    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
