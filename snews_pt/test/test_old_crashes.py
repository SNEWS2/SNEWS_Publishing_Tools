"""Test publishing coincidence tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt.snews_pt_utils import is_snews_format

def test_colon_in_time():
    """Test with example of expected message type.
        If works properly both format of times should pass
    """
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='XENONnT', neutrino_time='2012-06-09T15:31:07.99891011', p_val=0.4,
                               firedrill_mode=True, testing="this is a test")
    for message in coin.messages:
        assert is_snews_format(message), "Message is not in the snews format"
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

# ------------------------------------------------------------------------------------------------------
    coin2 = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08:891011', p_val=0.4,
                                firedrill_mode=True, testing="this is a test")
    for message in coin2.messages:
        assert is_snews_format(message), "Message is not in the snews format"
    try:
        coin2.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

