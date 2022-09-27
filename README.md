# SNEWS Publishing Tool
<img src="docs/custom_logo.png" alt="snews_logo" width="200"/> 

[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
![testing](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/ubuntu20-py39.yml/badge.svg)
<br>See the docs at

|              |        |
| ------------ | ------ |
| **Docs:**    | https://snews-publishing-tools.readthedocs.io/en/latest/  |

This packages provides users with a Python API and CLI to publish observation messages to SNEWS

> Note: Make sure your hop credentials are set up !!<br>
> Follow the instructions [**here**](https://github.com/scimma/hop-client) if needed<br>
> Request permissions to given topics [here](https://my.hop.scimma.org/hopauth/)

|                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| **Fire-Drills**                                                                                                                                                                                                                                                                                                                                                                                                 |
| Also see [this page](https://snews-publishing-tools.readthedocs.io/en/latest/user/firedrills.html)                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                            |
| `snews_pt` allows for fire-drill mode, currently this is the default option. <br/>Later, it can be adjusted through `firedrill_mode=True/False` arguments in subcription and publication functions, and through `--firedrill/--no-firedrill` flags within the CLI tools. Make sure you have the correct [permissions](https://my.hop.scimma.org/hopauth/) to publish and subscribe to these firedrill channels. |

## How to Install

- #### From source <br>
  First you need to clone this repo. In your terminal run the following:

  ```bash 
  git clone https://github.com/SNEWS2/SNEWS_Publishing_Tools.git
  ```
  Once cloned, install the package using pip (make sure you're in the cloned dir)
  ```bash
  pip install .
  ```

- #### From PyPi <br>
  ```bash
  pip install -U snews-pt
  ```

## How to Publish

Before we get started, right now the publishing method will send your message to the test kafka server.

First you need to import your Publisher:

````Python
# Import the constructor for SNEWS Tiers and Publisher class
from snews_pt.snews_pub import SNEWSTiersPublisher
````
### Passing Message Parameters as Arguments. 
To send a message you need initialize the ``Publisher``, construct your message by initializing ``SNEWSTiers`` and
passing your parameters of choice. The backend will parse your arguments, check their data types and determine which
tiers you can send a message to (see **Publishing Protocols**). If you pass multiple parameters (_see code bellow_) the
sender will send a message *all* the appropriate tiers.

```python
SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time="2022-02-28T04:31:08.678999",
                    timing_series=["2022-02-28T04:31:08.694999", "2022-02-28T04:31:08.698999", "2022-02-28T04:31:08.7078945"],
                    p_val=0.000007,
                    machine_time="2022-02-28T04:31:09.778859", 
                    ).send_to_snews()
```

This instance has parameters for **CoincidenceTier** and **TimingTier**, thus it will send a message to both. The output
should look like this:
![img.png](img.png)

### Passing Message Parameters from JSON File.

You can also pass your input from a json file, and make modifications on the spot. Let's first create an `observation` object this time before sending it to snews;

```python
observation = SNEWSTiersPublisher.from_json('my_input_asjson.json', 
                                            detector_name='XENONnT', 
                                            comment="This is submitted from a json file")
```
Here, we read the content from the `'my_input_asjson.json'` file, and overwrite `detector_name` and also add a comment field (which will be accepted as a meta data). Notice we still haven't sent it to snews yet. You can display, and modify the _parsed messages_ after you create the object instance. Depending on the fields you provided `SNEWSTierPublisher` will decide where to submit your data (see above). You can see these tier(s) and the individual message contents. See, `observation.tiernames` to get names of the tiers that your input message belongs, and `observation.messages` to display their content, and modify if desired.

Once you are done, you can just send that `observation` object to snews.

```
observation.send_to_snews()
```


***See this [`examples notebook`](./examples.ipynb) for more tutorial scripts***

- ### [See Publishing Protocols here](docs/user/message_schema.md)
- ### [See Message Schemas here](docs/user/message_schema.md)

## How to Subscribe

In two lines, one can subscribe to the alert topic specified in the default configuration. <br>
This starts a stream, and waits for alert messages to be received.

```python
from snews_pt.snews_sub import Subscriber

Subscriber().subscribe()
```

Should there be an alert message, this will be both displayed on the screen and saved into your local machine. The location can be passed as an argument `subscribe(outputfolder='folder/path')`, if not given, the default is used based on the `"ALERT_OUTPUT"` folder in the environment file. The message is then saved under this directory with a time stamp as `folder/0_<date>_ALERTS.json` and if there are multiple messages in the same day e.g. for the same supernova you kept receiving alerts with every coincidence message, the counter infront will be incremented. An example alert message (partly missing) can be
found [here](https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/doc/subscribed_messages.json)

---

# [Command Line Interface (CLI)](docs/cli_docs.md)

There also exists tools for command line interactions. These are explained in detail [here](docs/cli_docs.md)

### Extension for follow-up plugins (only with CLI for now)
`snews_pt subscribe` also allows for other scripts to be plugged in and act on alerts. The *CLI* command `snews_pt subscribe` takes the custom made script via `--plugin` (`-p`) option.

```bash 
user/home$: snews_pt subscribe -p ./auxiliary/custom_script.py
```

`snews_pt subscribe` saves the alert messages to a local JSON file with the date stamp of the received time. When a custom plugin is provided, as soon as an alert is received and JSON is created, the name of this unique-JSON file is passed to the script and executed.

Therefore, all custom-made scripts should contain the following two lines;

```python
# in "custom_made_script.py"
import sys, json
data = json.load(open(sys.argv[1]))
```
and do the follow-up work using the `data` dictionary as the alert message. See [this dummy example]https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/snews_pt/test/random_plugin.py) which 
only brags about itself and displays you the content of the alert message.

