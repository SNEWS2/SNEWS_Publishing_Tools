"""Test publishing significane tier messages."""
from SNEWS_PT.snews_pub import SNEWSTiersPublisher


def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSTiersPublisher(detector_name='DS-20K',
                               neutrino_times=['12/06/09 15:31:08:1098', 
                                               '12/06/09 15:33:07:8910'],
                               p_values=[0.4, 0.5],
                               t_bin_width=0.8)

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
                                 'meta': {'neutrino_times':
                                          ['12/06/09 15:31:08:1098',
                                           '12/06/09 15:33:07:8910']}}
    assert sign.messages == [
                            {'_id': '18_SigTier_None',
                             'detector_name': 'DS-20K',
                             'machine_time': None,
                             'neutrino_time': None,
                             't_bin_width': 0.8,
                             'p_values': [0.4, 0.5],
                             'meta': {'meta': {'neutrino_times':
                                               ['12/06/09 15:31:08:1098',
                                                '12/06/09 15:33:07:8910']}},
                             'schema_version': '1.1.0'}]
    assert sign.env_file is None

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
