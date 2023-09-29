"""Test publishing heartbeat messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_heartbeat_expected():
    """Test with example of expected message type."""
    # Create heartbeat tier message.
    hb = SNEWSMessageBuilder(detector_name='XENONnT', machine_time='2012-06-09T15:30:00.000501',
                             detector_status='ON',
                             firedrill_mode=False, is_test=True)
    # Check that message has expected structure.
    assert hb.selected_tiers == ['SNEWSHeartbeatMessage']
    assert len(hb.messages) == 1, f"Expected 1 Heartbeat Message got {len(hb.messages)}!"

    assert hb.messages[0].message_data == {'_id': 'XENONnT_Heartbeat_2012-06-09T15:30:00.000501',
                                           'schema_version': '1.3.0',
                                           'detector_name': 'XENONnT',
                                           'machine_time': '2012-06-09T15:30:00.000501',
                                           'detector_status': 'ON'}
    assert hb.messages[0].meta == {'is_test': True, 'firedrill_mode': False}

    # # check if valid snews format
    assert hb.messages[0].is_valid() is True, "Message is not valid"

    # Try to send message to SNEWS 2.0 server.
    try:
        hb.send_messages()
    except Exception as exc:
        print('SNEWSMessageBuilder.send_messages() test failed!\n')
        assert False, f"Exception raised:\n {exc}"