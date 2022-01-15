from SNEWS_PT.snews_pub import CoincidenceTier

def test_CoincidenceTier_message_keys():
    """Test creating a message with an invalid detector."""
    message = CoincidenceTier(detector_name='TEST', neutrino_time="01:23:45:678901", p_value=0.01).message()
    assert message['detector_name'] == 'TEST'
    assert message['neutrino_time'] == '01:23:45:678901'
    assert message['p_value'] == 0.01