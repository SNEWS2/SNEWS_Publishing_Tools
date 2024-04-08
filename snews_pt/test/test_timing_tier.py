"""Test publishing timing tier messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_timing_expected():
    """Test with example of expected message type."""
    # Create timing tier message.
    tims = SNEWSMessageBuilder(detector_name='XENONnT',
                               timing_series=['2012-06-09T15:31:08.109876', '2012-06-09T15:33:07.891011',
                                              '2012-06-09T15:33:07.9910110', '2012-06-09T15:34:07.891011000',
                                              '2012-06-09T15:35:17.0'],
                               machine_time='2012-06-09T15:30:00.009876',
                               firedrill_mode=False, is_test=True)

    # # Check that message has expected structure.
    assert tims.selected_tiers == ['SNEWSTimingTierMessage']
    assert tims.messages[0].message_data == {'_id': 'XENONnT_TimingTier_2012-06-09T15:30:00.009876000',
                                             'schema_version': '1.3.1',
                                             'detector_name': 'XENONnT',
                                             'machine_time': '2012-06-09T15:30:00.009876000',
                                             'p_val': None,
                                             'is_test': True,
                                             'timing_series': [0, 119781135000, 119881135000,
                                                               179781135000, 248890124000]}
    assert tims.messages[0].meta == { 'firedrill_mode': False}

    assert tims.messages[0].is_valid() is True, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        tims.send_messages()
    except Exception as exc:
        print('SNEWSMessageBuilder.send_messages() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

def test_timing_expected_with_floats():
    """Test with example of expected message type."""
    # Create timing tier message.
    tims = SNEWSMessageBuilder(detector_name='XENONnT',
                               timing_series=[0, 119781135000, 119881135000,
                                              179781135000, 248890124000],
                               machine_time='2012-06-09T15:30:00.009876',
                               firedrill_mode=False, is_test=True)

    # # Check that message has expected structure.
    assert tims.selected_tiers == ['SNEWSTimingTierMessage']
    assert tims.messages[0].message_data == {'_id': 'XENONnT_TimingTier_2012-06-09T15:30:00.009876000',
                                             'schema_version': '1.3.1',
                                             'detector_name': 'XENONnT',
                                             'machine_time': '2012-06-09T15:30:00.009876000',
                                             'p_val': None,
                                             'is_test': True,
                                             'timing_series': [0, 119781135000, 119881135000,
                                                               179781135000, 248890124000]}
    assert tims.messages[0].meta == { 'firedrill_mode': False}

    assert tims.messages[0].is_valid() is True, "There are invalid messages"

    # Try to send message to SNEWS 2.0 server.
    try:
        tims.send_messages()
    except Exception as exc:
        print('SNEWSMessageBuilder.send_messages() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
