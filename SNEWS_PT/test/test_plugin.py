import os
import signal
import subprocess

def test_subscribe_and_direct():
    # Subscribe to SNEWS alters in a subprocess via CLI.
    p = subprocess.Popen(['snews_pt', 'subscribe', '-p random_plugin.py'], stdout=subprocess.PIPE, shell=False, preexec_fn=os.setsid) 

    # List for SNEWS_PT echos
    echos = []
    for i in range(2):
        line = p.stdout.readline()
        echos.append(line)
    # Send 'ctrl + c' to process
    os.killpg(os.getpgid(p.pid), signal.SIGTERM) 

    assert echos[0] == b'You are subscribing to ALERT\n'
    assert echos[1] == b'Broker:kafka://kafka.scimma.org/snews.alert-test\n'

    # need to think of a better way to test this
    # assert echos[0] == b'Received alert\n'
    # assert echos[1] == b'Parsed as a dictionary\n'
