"""Test publishing coincidence tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt.snews_format_checker import SnewsFormat


def test_colon_in_time():
    """Test with example of expected message type.
        If works properly both format of times should pass
    """
    # Create coincidence tier message.
    coin = SNEWSTiersPublisher(detector_name='XENONnT', neutrino_time='2012-06-09T15:31:07.891011', p_val=0.4,
                               firedrill_mode=False, is_test=True)

    # the SNEWSTierPublisher already checks this in creation, but we can double check
    for message in coin.messages:
        format_checker = SnewsFormat(message)
        assert format_checker() is True, "Message is not in the snews format"
    try:
        coin.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

# ------------------------------------------------------------------------------------------------------
    coin2 = SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08:891011', p_val=0.4,
                                firedrill_mode=False, is_test=True)

    # the SNEWSTierPublisher already checks this in creation, but we can double check
    for message in coin2.messages:
        format_checker = SnewsFormat(message)
        assert format_checker() is True, "Message is not in the snews format"
    try:
        coin2.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

