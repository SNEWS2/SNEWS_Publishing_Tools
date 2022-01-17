from SNEWS_PT.snews_pub import Publisher
from SNEWS_PT.snews_pub import CoincidenceTier
from SNEWS_PT.snews_pub import TimingTier

def test_send_CoincidenceTier_working():
    """Test sending a coincidence tier message.
    
    Note
    ----
    Checks if SNEWS_PT can import, run, and connect to kafka.  Does not check for accuracy.
    """
    with Publisher() as pub:
        message = CoincidenceTier(detector_name='TEST', neutrino_time="01:23:45:678901", p_value = 0.01).message()
        pub.send(message)
    pass

def test_send_TimingTier_working():
    """Test sending a timing tier message.
    
    Note
    ----
    Checks if SNEWS_PT can import and run.  Does not check for accuracy.
    """
    with Publisher() as pub:
        message = TimingTier(detector_name='TEST', neutrino_time="01:23:45:678901", timing_series='time-series').message()
        pub.send(message)
    pass

def test_CoincidenceTier_message_keys():
    """Test creating a message with an invalid detector."""
    message = CoincidenceTier(detector_name='TEST', neutrino_time="01:23:45:678901", p_value=0.01).message()
    assert message['detector_name'] == 'TEST'
    assert message['neutrino_time'] == '01:23:45:678901'
    assert message['p_value'] == 0.01