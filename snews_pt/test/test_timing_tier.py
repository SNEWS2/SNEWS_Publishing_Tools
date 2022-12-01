"""Test publishing timing tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt.snews_format_checker import SnewsFormat


def test_timing_expected():
    """Test with example of expected message type."""
    # Create timing tier message.
    tims = SNEWSTiersPublisher(detector_name='XENONnT', neutrino_time='2012-06-09T15:31:08.109876',
                               timing_series=['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'],
                               firedrill_mode=False, is_test=True)

    # Check that message has expected structure.
    assert list(tims.tiernames) == ['CoincidenceTier', 'TimeTier']
    assert tims.message_data == {'detector_name': 'XENONnT',  'machine_time': None,
                                 'neutrino_time': '2012-06-09T15:31:08.109876',  'p_val': None,
                                 'p_values': None,  't_bin_width': None,
                                 'timing_series': ['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'],
                                 'which_tier': None, 'retract_latest': None, 'retraction_reason': None,
                                 'detector_status': None, 'is_pre_sn': False, 'is_test':True}
    assert tims.env_file == None

    # the SNEWSTierPublisher already checks this in creation, but we can double check
    for message in tims.messages:
        format_checker = SnewsFormat(message)
        assert format_checker() is True, "Message is not in the snews format"
    assert len(tims.invalid_messages) == 0, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        tims.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
