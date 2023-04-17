"""Test publishing coincidence tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt.snews_format_checker import SnewsFormat

def test_coincidence_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08.891011',
                               firedrill_mode=False, is_test=True)
    # Check that message has expected structure.
    assert list(coin.tiernames) == ['CoincidenceTier']
    assert len(coin.messages) == 1, f"Expected 1 CoincidenceTier Message got {len(coin.messages)}!"

    assert coin.message_data == {'detector_name': 'KamLAND', 'machine_time': None,
                                 'neutrino_time': '2012-06-09T15:31:08.891011',
                                 'p_val': None, 'p_values': None, 't_bin_width': None, 'timing_series': None,
                                 'retract_latest': None, 'retraction_reason': None,
                                 'detector_status': None, 'is_pre_sn': False, 'is_test':True}

    # the SNEWSTierPublisher already checks this in creation, but we can double check
    for message in coin.messages:
        format_checker = SnewsFormat(message)
        assert format_checker() is True, "Message is not in the snews format"

    assert len(coin.invalid_messages) == 0, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
