"""Test publishing significane tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt._version import version as __version__

def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSTiersPublisher(detector_name='DS-20K',
                               neutrino_times=['2012-06-09T15:31:08.109876', 
                                               '2012-06-09T15:33:07.891098'],
                               p_values=[0.4, 0.5],
                               t_bin_width=0.8,
                               firedrill_mode=False,
                               testing='this is a test')

    # Check that message has expected structure.
    assert sign.tiernames == ['SigTier']
    assert sign.message_data == {'detector_name': 'DS-20K',
                                 'machine_time': None,
                                 'neutrino_time': None,
                                 'p_val': None,
                                 'p_values': [0.4, 0.5],
                                 't_bin_width': 0.8,
                                 'timing_series': None,
                                 'which_tier': None,
                                 'n_retract_latest': None,
                                 'retraction_reason': None,
                                 'detector_status': None,
                                 'is_pre_sn': False,
                                 'neutrino_times':
                                          ['2012-06-09T15:31:08.109876',
                                           '2012-06-09T15:33:07.891098'],
                                 'testing': 'this is a test'}
    assert sign.env_file is None

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

test_significance_expected()