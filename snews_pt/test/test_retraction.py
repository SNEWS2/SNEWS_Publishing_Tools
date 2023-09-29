
"""Test publishing coincidence tier message and then retracting it"""
from snews_pt.messages import SNEWSMessageBuilder

def test_retraction():
    """Test with example of expected message type."""
    coin = SNEWSMessageBuilder(detector_name='KamLAND', neutrino_time='2012-06-09T15:31:08.891011',
                               firedrill_mode=False, is_test=True)

    # Check that message has expected structure.
    assert coin.selected_tiers == ["SNEWSCoincidenceTierMessage"]
    assert coin.messages[0].is_valid() is True, "Invalid coincidence message created"
    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_messages()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"

    # Now try to retract it
    retraction_message = SNEWSMessageBuilder(detector_name='KamLAND', retract_latest=1,
                                             machine_time='2012-06-09T15:30:00.000501',
                                             is_test=True, firedrill_mode=False)
    assert retraction_message.selected_tiers == ["SNEWSRetractionMessage"]
    assert retraction_message.messages[0].message_data == {'_id': 'KamLAND_Retraction_2012-06-09T15:30:00.000501',
                                                           'schema_version': '1.3.0',
                                                           'detector_name': 'KamLAND',
                                                           'machine_time': '2012-06-09T15:30:00.000501',
                                                           'retract_latest': 1,
                                                           'retraction_reason': None}, "created message data is wrong"
    assert retraction_message.messages[0].meta == {'is_test': True, 'firedrill_mode': False}, "created meta is wrong"
    assert retraction_message.messages[0].is_valid() is True, "Invalid retraction message created"

    try:
        # we can only test if the retraction message is send, not if it really retracted.
        retraction_message.send_messages()
    except Exception as exc:
        print('Retraction test failed!\n')
        assert False, f"Exception raised:\n {exc}"