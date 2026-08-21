# Publishing Protocols

One of the main functionality of the software is to publish messages to the SNEWS server. The exact protocols are also described in [the article](https://arxiv.org/abs/2406.17743).

The observation messages are generated using the `snews.messages` module. 
The `create_messages()` function is used to create messages for different tiers. It is flexible and minimizes the tasks for user by identifying tiers based on the given inputs. 
Different fields, and their formats as well as what tier message they trigger are shown below.


**Table 1** <br>

| Field                       | Format                  | Coincidence          | Significance         | Timing              | Heartbeats          | Retraction          |
|-----------------------------|-------------------------|----------------------|----------------------|---------------------|---------------------|---------------------|
| detector name               | str                     | **Required***        | **Required***        | **Required***       | **Required***       | **Required***       |
| initial neutrino time       | str                     | **Required**         | -                    | **Required**        | -                   | -                   |
| machine time                | str                     | Optional             | Optional             | Optional            | Optional            | Optional            |
| observation p-value         | float [0,1]             | Optional             | Optional             | Optional            | -                   | -                   |
| p-values for time bins      | list [float]            | -                    | **Required**         | -                   | -                   | -                   |
| width of time bins          | float                   | -                    | **Required**         | -                   | -                   | -                   |
| neutrino time series (histograms) | list [str (int)] | -                    | -                    | **Required**        | -                   | -                   |
| detector status             | str "ON"|"OFF"          | -                    | -                    | -                   | **Required**        | -                   |
| retract latest              | int                     | -                    | -                    | -                   | -                   | -                   |

User can also pass additional information under the `meta` field.

As an example, the following code creates a message for the Coincidence Tier and sends it to the SNEWS server.
```python
from snews_pt import messages 
from snews_pt.messages import Publisher

sn_msg = messages.create_messages(
  detector_name='LZ', 
  neutrino_time_utc="2022-02-28T04:31:08.678999",
  firedrill_mode=True,
  is_test=True,)
  
publisher = Publisher(kafka_topic=os.getenv("OBSERVATION_TOPIC"))
[publisher.add_message(message) for message in sn_msg_3]

publisher.send(verbose = True)
```

Since in this example, only the `neutrino_time_utc` and the `detector_name` is passed, the message is created for the Coincidence Tier. 
[TODO] This also assumes that the detector name has already been set by `snews_pt.snews_pt_utils.set_name()` function.

The messages are validated upon creation and if the required fields are not passed, or the format is wrong the software raises an error.
Furthermore, the `publisher` object can be inspected before sending them to the SNEWS server. It contains information about the selected tiers and the generated messages. THe list of messages to send can be accessed at `publisher.message_queue`.

The messages can also be created using a json file. The following command sends the message in the file `myjsonfile.json` to the SNEWS server.

```python
from snews import messages
from snews_pt.messages import Publisher
import json

with open('myjsonfile.json', "r", encoding="utf-8") as json_file:
    json_data = json.load(
        json_file
    )
sn_msg = messages.create_messages(**json_data)
[publisher.add_message(message) for message in sn_msg]
publisher.send(verbose=True)
```

Where the `myjsonfile.json` contains the following information;
```json
{
  "detector_name" : "LZ",
  "neutrino_time_utc" : "2022-02-28T04:31:08.678999",
  "is_test" : "True"
}
```

The `send()` method sends all of the created messages to the server and can give feedback with the argument `verbose=True`.

The `firedrill_mode` is set as part of each message and is used to select the firedrill topic from the environment (configuration) file,
`env_file` is the path to the environment file (by default uses the bundled profile from `auxiliary/dev-config.env` / `auxiliary/prod-config.env` based on `BROKER_MODE`).


The same functionalities can be achieved using the command line interface. The following command sends the message in the file `myjsonfile.json` to the SNEWS server.
```bash
snews_pt publish myjsonfile.json --firedrill
```
