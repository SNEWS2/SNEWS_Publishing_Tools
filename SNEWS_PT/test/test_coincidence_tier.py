"""Test publishing coincidence tier messages."""
from SNEWS_PT.snews_pub import SNEWSTiersPublisher

def test_coincidence_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='12/06/09 15:31:08:1098', p_value=0.4)
    # Check that message has expected structure.
    assert coin.tiernames == ['CoincidenceTier']
    assert coin.args_dict == {'detector_name': 'KamLAND', 'neutrino_time': '12/06/09 15:31:08:1098', 'p_value': 0.4, 'is_pre_sn': False}
    assert coin.messages == [{'_id': '4_CoincidenceTier_None', 'detector_name': 'KamLAND', 'machine_time': None, 'schema_version': '1.0.1', 'neutrino_time': '12/06/09 15:31:08:1098', 'p_val': None, 'meta': {'p_value': 0.4}}]
    assert coin.env_file == None
    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
