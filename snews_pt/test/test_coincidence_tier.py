"""Test publishing coincidence tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt._version import version as __version__


def test_coincidence_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08.891011', p_value=0.4,
                               firedrill_mode=False, testing="this is a test")
    # Check that message has expected structure.
    assert coin.tiernames == ['CoincidenceTier']
    assert coin.message_data == {'detector_name': 'KamLAND', 'machine_time': None, 'neutrino_time': '2012-06-09T15:31:08.891011', 
                                 'p_val': None, 'p_values': None, 'timing_series': None, 'which_tier': None, 'n_retract_latest': None, 
                                 'retraction_reason': None, 'detector_status': None, 'is_pre_sn': False, 't_bin_width': None,
                                 'p_value': 0.4, 'testing': 'this is a test'}

    assert coin.env_file == None
    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
