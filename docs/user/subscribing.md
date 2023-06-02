# Subscribing

`snews_pt` allows its users to subscribe several kafka topics to be alerted when there is a coincidence found between at least two of the participating detectors.

If you followed the [installation](./installation.md) guide and the [quick start](./quickstart.md) you should 
already have the packages `hop` and `snews_pt`. 

Test them on your terminal;
```bash
hop --version
snews_pt --version
```

If you get an error, go back to [installation](./installation.md) guide and the [quick start](./quickstart.md).

## Python API

Subscribing is a peristent instance, meaning that, once you subscribe, 
it keeps listening the channel until it is interrupted.

On a jupyter notebook you can subscribe to an alert topic by running the following;

```python
from snews_pt.snews_sub import Subscriber
Subscriber().subscribe()
```

This opens a kafka stream and waits for messages. Once an alert message is received, it is saved locally, and the subscriber keeps
on running to look for more updates. You can specify the output folder by passing `outputfolder="your_path/"`. 
By default it subscribes to the firedrill topic. This can be changed by passing `firedrill_mode=False` to the `Subscriber()`.

So an alternative subscription might look like;
```python
Subscriber(firedrill_mode=False).subscribe(outputfolder="./different_folder/")
```

## Command Line Interface

The same functionalities, plus a useful plugin functionality can also be found within CLI.

```bash
snews_pt subscribe -o ./this_folder/ --firedrill
------------------ OR
snews_pt subscribe -o ./this_folder/ --no-firedrill
```

Since the `subscribe` is a persistent method, we provide a mechanism that allows you to use **follow-up scripts**.
To do that you take your `custom_script.py` and add the following two lines;

```python
import sys, json
data = json.load(open(sys.argv[1]))
```
Then, when you subscribe you point to your script;

```bash
snews_pt subscribe --no-firedrill -p custom_script.py
```

Now, you subscribe to the alerts, and whenever there is an alert the output is saved to your local machine,
then while your terminal keeps listening the topic, a separate instance calls your `custom_script.py` and tells the script about the filename of the latest alert.
The lines you added reads this file as a dictionary. From there you can use the dictionary to perform 
any follow-up tasks.

The alert content should look like;

```python
{"_id": "id",
 "alert_type": "INITIAL/UPDATE/RETRACTION",
 "server_tag": "Purdue Server",
 "False Alarm Prob": "0.5%",
 "detector_names": ["detector A", "detector B"],
 "sent_time": "time string in ISO-Format",
 "p_values": [0.7, 0.85],
 "neutrino_times": ["time string1", "time string2"],
 "p_values average": 0.775,
 "sub list number": 0}
```



