""" This is a random plugin to test `subscribe_and_redirect_alert """
import sys
import json

# It takes the alert message as a first input
print(f"Received alert")
alert_message = json.loads(sys.argv[1])
print(f"Parsed as a dictionary")
print(f"Running custom plugin {sys.argv[0]}")
print(f"There are these keys; {alert_message.keys()}")
print(f"The message content is \n {alert_message}")
print(f"Do fancy stuff here with the freshly baked alert message")
