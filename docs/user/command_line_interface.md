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
  get-feedback    Get an e-mail feedback on your heartbeats
  heartbeat       Publish heartbeat messages.
  message-schema  Display the message format for `tier`, default 'all'
  publish         Publish a message using snews_pub
  retract         Retract N latest message
  subscribe       Subscribe to Alert topic 
  set-name        Set your detectors name
  reset-cache     Development purposes only, requires admin pass
  run-scenarios   Test different coincidence scenarios
  test-connection Test the server connection
  write-hb-logs   Development purposes only, requires admin pass
```

The main command `snews_pt` serves an entry point. It is also possible to set an _environment_ by passing it to this with any other command. 
E.g. `snews_pt --env myenvfile.env subscribe` will set the variables in _myenvfile.env_  and subscribe to the _ALERT_TOPIC_ specified in this file. <br>
By default, it uses the environment file that comes with the package.

For any command the help can be displayed 
```bash
(venv) User$: snews_pt <COMMAND> --help
```
---
## Subscribing to Alert Topics
The subscription command can be called without any arguments.
```bash 
(venv) User$: snews_pt subscribe --no-firedrill
> You are subscribing to ALERT 
> Broker:kafka://kafka.scimma.org/snews.alert
```
```bash 
(venv) User$: snews_pt subscribe --firedrill
> You are subscribing to ALERT 
> Broker:kafka://kafka.scimma.org/snews.alert-test
```

---
## Sending Heartbeats
```bash 
(venv) User$: snews_pt heartbeat -s ON -t "2023-06-02T09:27:40.882808" --firedrill
Message Generated for Heartbeat                                                                                         
----------------------------------------------------------------
Sending message to Heartbeat on kafka://kafka.scimma.org/snews.experiments-firedrill
_id                :19_Heartbeat_2023-06-02T09:27:40.882808
detector_name      :XENONnT
machine_time       :2023-06-02T09:27:40.882808                                                                          
detector_status    :ON
meta               :
schema_version     :1.3.0
sent_time          :2023-06-02T09:48:13.393969
```

Here the machine time refers to the time your experiment reads the data that sets ON or OFF status. There can be 
instances where this data has been read but could not be send to server right away, therefore, the `sent_time` is stamped at the execution.

## Message Schemas
`snews_pt message-schema` can tell you the required contents for each tiers. You can display the contents of a single tier by calling e.g.
```bash
(venv) User$: snews_pt message-schema CoincidenceTier
```
In which case it displays the following
```bash
         > Message schema for CoincidenceTier
         id                   : (USER INPUT)
         uuid                 : (USER INPUT)
         tier                 : (REQUIRED USER INPUT)
         sent_time_utc        : (USER INPUT)
         machine_time_utc     : (USER INPUT)
         is_pre_sn            : (USER INPUT)
         is_test              : (USER INPUT)
         is_firedrill         : (USER INPUT)
         meta                 : (USER INPUT)
         schema_version       : (USER INPUT)
         detector_name        : (REQUIRED USER INPUT)
         p_val                : (USER INPUT)
         neutrino_time_utc    : (REQUIRED USER INPUT)
         **kwargs             : (GROUPED AS META)
```
or you can simply call `snews_pt message-schema all`  to display all the message schemes. <br>

---

## Publishing Observation Messages
User can also publish observation messages using the command line interface. 
For that user has to have a JSON file with the proper key-value pairs. `snews_pt` python API also allows for saving the message content as a json once you create a message using `SNEWSTierPublisher`. 
The simplest JSON file that you can publish using the CLI would contain the following;
```json
# in my_message.json
{
    "detector_name":
        "DUNE",
    "neutrino_time_utc":
        "2025-10-30T15:44:12.345275"
}
```
In which case, only the `"neutrino_time"` argument is parsed and the CoincidenceTierPublisher is invoked.

**Publish using the CLI**
```bash
(venv) User$: snews_pt publish my_message.json --firedrill

Message Generated for CoincidenceTier
----------------------------------------------------------------
Sending message to CoincidenceTier on kafka://kafka.scimma.org/snews.experiments-firedrill
_id                :19_CoincidenceTier_2023-06-02T10:04:27.400593
detector_name      :XENONnT
machine_time       :2023-06-02T10:04:27.400593
neutrino_time      :2023-06-02T09:48:13.393969
p_val              :None
meta               :
is_test            :False
schema_version     :1.3.0
sent_time          :2023-06-02T10:04:27.461761 
```

## Retraction Messages

It can happen that user publishes a message by accident or with wrong input. In these cases `snews_pt` allows for retraction messages. 
These are also messages created by `SNEWSTierPublisher` with some specific keys. <br>
Let's first check what arguments belong to retraction message.

```bash
$ snews_pt message-schema Retraction
Message schema for Retraction
id                   : (USER INPUT)
uuid                 : (USER INPUT)
tier                 : (REQUIRED USER INPUT)
sent_time_utc        : (USER INPUT)
machine_time_utc     : (USER INPUT)
is_pre_sn            : (USER INPUT)
is_test              : (USER INPUT)
is_firedrill         : (USER INPUT)
meta                 : (USER INPUT)
schema_version       : (USER INPUT)
detector_name        : (REQUIRED USER INPUT)
retract_message_uuid : (USER INPUT)
retract_latest_n     : (USER INPUT)
retraction_reason    : (USER INPUT)
**kwargs             : (GROUPED AS META)
```
The fields with REQUIRED USER INPUT are the keywords that are needed to select this tier. In this case, input should have `retract_latest_n` key in order to create a retraction message for the last two messages from the detector named `DUNE` 
```json
# in retract_message.json
{
  "detector_name": "DUNE",
  "retract_latest_n" : 2
}
```

```bash
(venv) User$: snews_pt publish retract_message.json --firedrill
Message Generated for Retraction
----------------------------------------------------------------
Sending message to Retraction on kafka://kafka.scimma.org/snews.experiments-firedrill
IT'S OKAY, WE ALL MAKE MISTAKES
_id                :19_Retraction_2023-06-02T10:12:01.001552
detector_name      :XENONnT
machine_time       :2023-06-02T10:12:01.001552
retract_latest     :2
retraction_reason  :None
meta               :
is_test            :False
schema_version     :1.3.0
sent_time          :2023-06-02T10:12:01.049846 
```
