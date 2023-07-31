
"""Test connection with the server."""
from snews_pt.remote_commands import test_connection

def test_connection_to_server():
    """Test connection with the server."""
    assert test_connection(detector_name="XENONnT", firedrill=False, start_at="LATEST", patience=8) is True, "Connection to server failed on no-firedrill broker!"