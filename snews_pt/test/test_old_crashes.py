"""Test publishing coincidence tier messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_colon_in_time():
    """Test with example of expected message type.
        If works properly both format of times should pass
    """
    # Create coincidence tier message.
    coin = SNEWSMessageBuilder(detector_name='XENONnT', neutrino_time='2012-06-09T15:31:07.891011', p_val=0.4,
                               firedrill_mode=False, is_test=True)

    # the SNEWSTierPublisher already checks this in creation, but we can double-check
    assert coin.messages[0].is_valid() is True, "dot separated neutrino time failed!"
    try:
        coin.send_messages()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

    # ------------------------------------------------------------------------------------------------------
    coin2 = SNEWSMessageBuilder(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08:891011', p_val=0.4,
                                firedrill_mode=False, is_test=True)

    # the SNEWSTierPublisher already checks this in creation, but we can double-check
    assert coin2.messages[0].is_valid() is True, "Semicolon separated neutrino time failed!"
    try:
        coin2.send_messages()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

