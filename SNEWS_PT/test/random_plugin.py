""" This is a random plugin to test `subscribe_and_redirect_alert """

# This part needs to be in all of the plugins
import sys
import json
saved_json = sys.argv[1]
this_plugin = sys.argv[0]
data = json.load(open(saved_json))


# Later, user can do whatever they want with the data
# here is an example.
# Say, for each alert message, I want to write the names of the detectors
# and the neutrino time to file called demofile.txt

from datetime import datetime
import os

now = datetime.utcnow().strftime("%H:%M:%S")
f = open(os.path.join(os.getcwd(), "demofile.txt"), "a")

f.write(f"\nNow time is {now} the file has more content!\n\n")
f.write(f"Received alert {saved_json}\n")
f.write(f"Do some fancy stuff. it is a python dictionary with pre-determined (ALERT Tier) keys")
f.write(f"Running custom plugin {this_plugin}\n")
f.write(f"There were {len(data.keys())} experiments contributing to this alert\n")
f.write(f"They are; {data['detector_names']}\n")
pvalues = [float(i) for i in data['p_values']]
f.write(f"The sum of their p values are {sum(pvalues)}\n")
f.write(f"Here is the message content is \n {data}\n")
f.close()
