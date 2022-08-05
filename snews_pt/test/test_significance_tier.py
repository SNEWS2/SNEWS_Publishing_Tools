"""Test publishing significane tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher

def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSTiersPublisher(detector_name='DS-20K',
                               neutrino_times=['2012-06-09T15:31:08.1098', 
                                               '2012-06-09T15:33:07.8910'],
                               p_values=[0.4, 0.5],
                               t_bin_width=0.8,
                               firedrill_mode=False)

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
                                          ['2012-06-09T15:31:08.1098',
                                           '2012-06-09T15:33:07.8910']}
    input_message = {'detector_name': 'DS-20K',
                     'machine_time': None,
                     'neutrino_time': None,
                     't_bin_width': 0.8,
                     'p_values': [0.4, 0.5],
                     'meta': {'neutrino_times':
                                   ['2012-06-09T15:31:08.1098',
                                    '2012-06-09T15:33:07.8910']},
                     'schema_version': '1.1.0'}
    for k,v in input_message.items():
        if k in ['sent_time', 'machine_time']:
            continue
        assert sign.messages[0][k] == v

    assert sign.env_file is None

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

test_significance_expected()