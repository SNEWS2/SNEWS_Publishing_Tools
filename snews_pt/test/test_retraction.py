
"""Test publishing coincidence tier message and then retracting it"""
from snews_pt.snews_pub import SNEWSTiersPublisher

def test_retraction():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08.891011',
                               firedrill_mode=False, is_test=True)

    # Check that message has expected structure.
    assert list(coin.tiernames) == ['CoincidenceTier']
    assert len(coin.messages) == 1, f"Expected 1 CoincidenceTier Message got {len(coin.messages)}!"
    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

    # Now try to retract it
    retraction_message = SNEWSTiersPublisher(detector_name='KamLAND', n_retract_latest=1, is_test=True)
    try:
        # we can only test if the retraction message is send, not if it really retracted.
        retraction_message.send_to_snews()
    except Exception as exc:
        print('Retraction test failed!\n')
        assert False, f"Exception raised:\n {exc}"