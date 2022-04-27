# Command Line Interface (CLI)

It is also possible to interact with `snews_pt` through the command line. <br>
All the commands have their short descriptions accessible via `--help` flag. 
```bash
(venv) User$: snews_pt --help 
```
```bash
Usage: snews_pt [OPTIONS] COMMAND [ARGS]...
  User interface for snews_pt tools

Options:
  --version   Show the version and exit.
  --env TEXT  environment file containing the configurations  [default: (auxiliary/test-config.env)]
  --help      Show this message and exit.

Commands:
  message-schema  Display the message format for `tier`, default 'all'
  publish         Publish a message using snews_pub
  subscribe       Subscribe to Alert topic 
```
The main command `snews_pt` serves an entry point. It is also possible to set an _environment_ by passing it to this with any other command. 
E.g. `snews_pt --env myenvfile.env subscribe` will set the variables in _myenvfile.env_  and subscribe to the _ALERT_TOPIC_ specified in this file. <br>
By default, it uses the environment file that comes with the package.

---
## Subscribing to Alert Topics
The subscription command can be called without any arguments.
```bash 
(venv) User$: snews_pt subscribe 
```
```bash
> You are subscribing to ALERT 
> Broker:kafka://kafka.scimma.org/snews.alert-test
```

**Fire-Drills**<br>
In case you want to subscribe to the firedrill channels, you can simply pass `--firedrill` in the command
and it will automatically use the existing firedrill channel.
```bash 
(venv) User$: snews_pt subscribe --firedrills
```

### Extension for follow-up plugins 
`snews_pt subscribe` also allows for other scripts to be plugged in and act on alerts. The *CLI* command `snews_pt subscribe` takes the custom made script via `--plugin` (`-p`) option.

```bash 
user/home$: snews_pt subscribe -p custom_made_script.py
```

`snews_pt subscribe` saves the alert messages to a local JSON file with the date stamp of the received time. When a custom plugin is provided, as soon as an alert is received and JSON is created, the name of this unique-JSON file is passed to the script and executed.

Therefore, all custom made scripts should contain the following two lines;

```python
# in "custom_made_script.py"
import sys, json
data = json.load(open(sys.argv[1]))
```
and do the follow-up work using the `data` dictionary as the alert message. See [this dummy example](https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/plug-in-scripts/SNEWS_PT/test/random_plugin.py).


---
## Message Schemas
`snews_pt message-schema` can tell you the required contents for each tiers. You can display the contents of a single tier by calling e.g.
```bash
(venv) User$: snews_pt message-schema time
```
In which case it displays the following
```bash
         >The Message Schema for TimeTier 
_id                 :(SNEWS SETS)
detector_name       :(SNEWS SETS)
sent_time           :(SNEWS SETS)
machine_time        :(User Input)
neutrino_time       :(User Input)
timing_series       :(User Input)  
```
or you can simply call `snews_pt message-schema` without any positional arguments in which case it displays all the message schemes. <br>

---

## Publishing Observation Messages
User can publish json format observation messages to 'CoincidenceTier', 'TimeTier', or 'SigTier'. It is also possible to publish _Heartbeat_ and _Retraction_ messages.
The tiers are decided based on the content of the input. Several `json` files are allowed

```bash
(venv) User$: snews_pt publish "myjsonfile.json" "mysecondfile.json"
```
The `publish` tool takes these json files and passed them to the `SNEWSTierPublisher` instance from the `snews_pub` module. As a result, the input file(s) are parsed and the tiers are determined. Next, the message content is created for these respective tier(s) and sent to snews subsequently. 

There are several dummy json examples [here](../test/) that can be used as a reference. Should you have key-value pairs that do not belong to any tier (see `snews_pt message-schema`), these are passed under `meta` field.

Try publishing the following file which contains an `extra_key` field.
```bash
(venv) User$: snews_pt publish SNEWS_PT/test/example_coincidence_tier_message.json
```

It should give the following
```bash
Publishing to CoincidenceTier;
---------------------------------------------------------
_id                 :0_CoincidenceTier_22/01/01_20:19:06:356690
detector_name       :TEST
sent_time           :22/01/01 20:19:06
machine_time        :test machine time
neutrino_time       :test nu time
p_value             :test p-values 
meta                :{'extra_key':'extra_value'}
```

**Fire-Drills**<br>
In case you want to publish to the firedrill channels, you can simply pass `--firedrill` in the command
and it will automatically use the existing firedrill channel.
```bash 
(venv) User$: snews_pt publish path/to/your_message.json --firedrills
```

----

## Publishing Heartbeat and Retraction messages

Similar to the observation messages heartbeat and retraction messages can be passed using a json file with the `snews_pt publish` command. In the next version, we are planning to provide more convenient tools for them.

## Run Scenarios (Testing Only)

We also have a simple interface to invoke several different coincidences using `snews_pt run-scenarios` command. When executed, it prompts a screen with several pre-designed coincidence scenarios from which user can select by clicking _right arrow key_ when on the scenario, and entering. This will submit the messages within that scenario and then clear the cache. If the coincidence system is running in the given test topic, these scenarios should trigger different types of alerts, and these alerts should be received in the _subscribed_ terminal. 

Notice that this is only for development and testing purposes and clears the cache after each scenario execution. This will not be a part of the actual snews topic.












