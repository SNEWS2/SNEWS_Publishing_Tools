"""Test publishing significane tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt.snews_format_checker import SnewsFormat

def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSTiersPublisher(detector_name='DS-20K',
                               neutrino_time = '2012-06-09T15:31:08.109876',
                               neutrino_times=['2012-06-09T15:31:08.109876', 
                                               '2012-06-09T15:33:07.891098'],
                               p_values=[0.4, 0.5],
                               t_bin_width=0.8,
                               firedrill_mode=False,
                               is_test=True)

    # Check that message has expected structure.
    assert list(sign.tiernames) == ['CoincidenceTier', 'SigTier']
    assert sign.message_data == {'detector_name': 'DS-20K',
                                'machine_time': None,
                                'neutrino_time': '2012-06-09T15:31:08.109876',
                                'p_val': None,
                                'p_values': [0.4, 0.5],
                                't_bin_width': 0.8,
                                'timing_series': None,
                                'retract_latest': None,
                                'retraction_reason': None,
                                'detector_status': None,
                                'is_pre_sn': False,
                                'neutrino_times': ['2012-06-09T15:31:08.109876',
                                                   '2012-06-09T15:33:07.891098'],
                                'is_test':True}
    assert sign.env_file is None

    # the SNEWSTierPublisher already checks this in creation, but we can double check
    for message in sign.messages:
        format_checker = SnewsFormat(message)
        assert format_checker() is True, "Message is not in the snews format"

    assert len(sign.invalid_messages)==0, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

test_significance_expected()