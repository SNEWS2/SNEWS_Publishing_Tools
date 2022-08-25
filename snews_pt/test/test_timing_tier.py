"""Test publishing timing tier messages."""
from snews_pt.snews_pub import SNEWSTiersPublisher
from snews_pt._version import version as __version__

def test_timing_expected():
    """Test with example of expected message type."""
    # Create timing tier message.
    tims = SNEWSTiersPublisher(detector_name='XENONnT', neutrino_time='2012-06-09T15:31:08.109876', timing_series=['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'],
                               firedrill_mode=False)

    # Check that message has expected structure.
    assert tims.tiernames == ['CoincidenceTier', 'TimeTier']
    assert tims.message_data == {'detector_name': 'XENONnT', 'machine_time': None, 'neutrino_time': '2012-06-09T15:31:08.109876', 'p_val': None, 'p_values': None,
                                 'timing_series': ['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'], 'which_tier': None, 'n_retract_latest': None,
                                 'retraction_reason': None, 'detector_status': None, 'is_pre_sn': False, 't_bin_width': None, }

    input_messages = [{'detector_name': 'XENONnT', 'machine_time': None, 'neutrino_time': '2012-06-09T15:31:08.109876',
                     'p_val': None, 'meta': {}, 'schema_version': __version__},
                      {'detector_name': 'XENONnT', 'machine_time': None,
                     'neutrino_time': '2012-06-09T15:31:08.109876',
                       'timing_series': ['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'],
                       'meta': {}, 'schema_version': __version__}]
    for i, message in enumerate(input_messages):
        for k,v in message.items():
            if k in ['sent_time', 'machine_time']:
                continue
            assert tims.messages[i][k] == v

    assert tims.env_file == None
    # Try to send message to SNEWS 2.0 server.
    try:
        tims.send_to_snews()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
