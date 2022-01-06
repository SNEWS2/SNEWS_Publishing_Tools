from SNEWS_PT.snews_pub import Publisher
from SNEWS_PT.snews_pub import CoincidenceTier

def test_send_CoincidenceTier_typical():
    """Test sending a typical coincidence tier message."""
    with Publisher() as pub:
        message = CoincidenceTier(detector_name='TEST', neutrino_time="01:23:45:678901", p_value = 0.01).message()
        pub.send(message)
    pass

def test_CoincidenceTier_message_basic():
    """Test creating a message with an invalid detector."""
    message = CoincidenceTier(detector_name='TEST', neutrino_time="01:23:45:678901", p_value = 0.01).message()
    assert message['detector_name'] == 'TEST'
    assert message['neutrino_time'] == '01:23:45:678901'
    assert message['p_value'] == 0.01