# Publishing Protocols

One of the main functionality of the software is to publish messages to the SNEWS server. The exact protocols are also described in [the article](https://arxiv.org/abs/2406.17743).

The observation messages are generated using the `snews_pt.messages` module. 
The `SNEWSMessageBuilder` class is used to create messages for different tiers. It is flexible and minimizes the tasks for user by identifying tiers based on the given inputs. 
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
from snews_pt.messages import SNEWSMessageBuilder

messages = SNEWSMessageBuilder(neutrino_time="2022-02-28T04:31:08.678999")
messages.send_messages()
```

Since in this example, only the `neutrino_time` is passed, the message is created for the Coincidence Tier. This also assumes that the detector name has already been set by `snews_pt.snews_pt_utils.set_name()` function.

The messages are validated upon creation and if the required fields are not passed, or the format is wrong the software raises an error.
Furthermore, the `messages` objects can be inspected before sending them to the SNEWS server. It contains information about the selected tiers and the generated messages.

The messages can also be created using a json file. The following command sends the message in the file `myjsonfile.json` to the SNEWS server.
```python
from snews_pt.messages import SNEWSMessageBuilder

messages = SNEWSMessageBuilder(jsonfile="myjsonfile.json")
messages.send_messages()
```

Where the `myjsonfile.json` contains the following information;
```json
{
  "neutrino_time" : "2022-02-28T04:31:08.678999"
}
```

The `send_messages` attribute sends all of the created messages to the server and has the following arguments;
```python
messages.send_messages(firedrill_mode=True, env_file=None, verbose=True, auth=True)
```
Where the `firedrill_mode` argument is used to select the firedrill topic from the environment (configuration) file,
`env_file` is the path to the environment file (by default uses [auxiliary/test-config.env](https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/snews_pt/auxiliary/test-config.env),
`verbose` is used to print the messages, and `auth` is used to authenticate the user credentials.


The same functionalities can be achieved using the command line interface. The following command sends the message in the file `myjsonfile.json` to the SNEWS server.
```bash
snews_pt publish myjsonfile.json --firedrill
```