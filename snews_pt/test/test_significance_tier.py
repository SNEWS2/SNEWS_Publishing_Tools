"""Test publishing significant tier messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_significance_expected():
    """Test with example of expected message type."""
    # Create significance tier message.
    sign = SNEWSMessageBuilder(detector_name='DS-20K',
                               machine_time='2012-06-09T15:30:00.000501',
                               neutrino_time='2012-06-09T15:31:08.109876',
                               neutrino_times=['2012-06-09T15:31:08.109876',
                                               '2012-06-09T15:33:07.891098'],
                               p_values=[0.4, 0.5],
                               t_bin_width=0.8,
                               firedrill_mode=False,
                               is_test=True)

    # Check that message has expected structure.
    assert sign.selected_tiers == ['SNEWSCoincidenceTierMessage', 'SNEWSSignificanceTierMessage']
    assert sign.messages[0].message_data == {'_id': 'DS-20K_CoincidenceTier_2012-06-09T15:30:00.000501',
                                             'schema_version': '1.3.0',
                                             'detector_name': 'DS-20K',
                                             'machine_time': '2012-06-09T15:30:00.000501',
                                             'neutrino_time': '2012-06-09T15:31:08.109876',
                                             'p_val': None}

    assert sign.messages[0].meta == {'p_values': [0.4, 0.5],
                                     't_bin_width': 0.8,
                                     'is_test': True,
                                     'neutrino_times': ['2012-06-09T15:31:08.109876',
                                                        '2012-06-09T15:33:07.891098'],
                                     'firedrill_mode': False}

    assert sign.messages[1].message_data == {'_id': 'DS-20K_SignificanceTier_2012-06-09T15:30:00.000501',
                                             'schema_version': '1.3.0',
                                             'detector_name': 'DS-20K',
                                             'machine_time': '2012-06-09T15:30:00.000501',
                                             'p_values': [0.4, 0.5],
                                             't_bin_width': 0.8}

    assert sign.messages[1].meta == {'neutrino_time': '2012-06-09T15:31:08.109876',
                                     'is_test': True,
                                     'neutrino_times': ['2012-06-09T15:31:08.109876',
                                                        '2012-06-09T15:33:07.891098'],
                                     'firedrill_mode': False}

    assert sign.messages[0].is_valid() is True, "invalid coincidence tier message in 'test_significance_tier'"
    assert sign.messages[1].is_valid() is True, "invalid significance tier message in 'test_significance_tier'"

    # Try to send message to SNEWS 2.0 server.
    try:
        sign.send_messages()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
