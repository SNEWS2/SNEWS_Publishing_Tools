"""Test publishing timing tier messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_timing_expected():
    """Test with example of expected message type."""
    # Create timing tier message.
    tims = SNEWSMessageBuilder(detector_name='XENONnT',
                               timing_series=['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011'],
                               machine_time='2012-06-09T15:30:00.009876',
                               firedrill_mode=False, is_test=True)

    # # Check that message has expected structure.
    assert tims.selected_tiers == ['SNEWSTimingTierMessage']
    assert tims.messages[0].message_data == {'_id': 'XENONnT_TimingTier_2012-06-09T15:30:00.009876',
                                             'schema_version': '1.3.0',
                                             'detector_name': 'XENONnT',
                                             'machine_time': '2012-06-09T15:30:00.009876',
                                             'p_val': None,
                                             'timing_series': ['2012-06-09T15:31:08.109876',
                                                               '2012-06-09T15:33:07.891011']}
    assert tims.messages[0].meta == {'is_test': True, 'firedrill_mode': False}

    assert tims.messages[0].is_valid() is True, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        tims.send_messages()
    except Exception as exc:
        print('SNEWSMessageBuilder.send_messages() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
