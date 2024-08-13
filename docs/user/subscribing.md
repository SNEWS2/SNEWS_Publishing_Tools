# Subscribing

One of the main functionalities of `snews_pt` is to subscribe to the alert topics. <br>
The software provides an easy way to subscribe to the alert topics and receive the alerts in real-time. <br>

This is done via the `Subscriber` class in the `snews_sub` module. <br>

```python
from snews_pt.snews_sub import Subscriber
Subscriber(env_path=None, firedrill_mode=True).subscribe(outputfolder=None, auth=True)
```

Where the `env_path` is the path to the environment file, `firedrill_mode` is a boolean to specify if the subscription is for a firedrill or not, `outputfolder` is the path to the folder where the alerts are saved, and `auth` is a boolean to specify if the user wants to authenticate the subscription.
This function is then starts listening the alerts from the given topic and once it finds a new message, it displays it on the screen, saves a json file with the alert content to the specified folder, and continues to listen for more messages until it is manually interrupted.

Same functionality can be accessed via the CLI tool as well. <br>
```bash
snews_pt subscribe -o ./this_folder/ --firedrill
------------------ OR
snews_pt subscribe -o ./this_folder/ --no-firedrill
```
## Subscribe and Redirect

Additionaly, `snews_pt` offers a way to subscribe to the alert topics and redirect the alerts to a custom script. <br>
This can only be done using the command line interface and requires some modification to the plug-in script. <br>

It simply calls the custom plugin script each time there is a new alert and passes the path to the json file containing the alert content. <br>
For this reason, the plugin script should be able to read the json file and perform the necessary actions. <br>

The plugin script should be in the following format: <br>
```python
# (custom_script.py)
import sys, json
data = json.load(open(sys.argv[1]))
# <perform specific tasks>
```

Then subscribe to the alert topics using the following command: <br>
```bash
snews_pt subscribe --no-firedrill -p custom_script.py
```
