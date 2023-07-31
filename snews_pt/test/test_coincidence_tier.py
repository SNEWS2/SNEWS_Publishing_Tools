"""Test publishing coincidence tier messages."""
from snews_pt.messages import SNEWSMessageBuilder

def test_coincidence_expected():
    """Test with example of expected message type."""
    # Create coincidence tier message.
    coin = SNEWSMessageBuilder(detector_name='KamLAND', machine_time='2012-06-09T15:30:00.000501',
                               neutrino_time='2012-06-09T15:31:08.891011',
                               firedrill_mode=False, is_test=True)
    # Check that message has expected structure.
    assert list(coin.selected_tiers) == ['SNEWSCoincidenceTierMessage']
    assert len(coin.messages) == 1, f"Expected 1 CoincidenceTier Message got {len(coin.messages)}!"

    assert coin.messages[0].message_data == {'_id': 'KamLAND_CoincidenceTier_2012-06-09T15:30:00.000501',
                                             'detector_name': 'KamLAND',
                                             'machine_time': '2012-06-09T15:30:00.000501',
                                             'schema_version': '1.3.0',
                                             'neutrino_time': '2012-06-09T15:31:08.891011',
                                             'p_val': None}
    assert coin.messages[0].meta == {'is_test': True, 'firedrill_mode': False}

    # check if valid snews format
    assert coin.messages[0].is_valid() is True, "Message is not valid"

    # Try to send message to SNEWS 2.0 server.
    try:
        coin.send_messages()
    except Exception as exc:
        print('SNEWSTiersPublisher.send_to_snews() test failed!\n')
        assert False, f"Exception raised:\n {exc}"
