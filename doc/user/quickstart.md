# Quickstart

The module allows you to `publish`, `subscribe`, `retract` and `simulate` observation messages among other things. For these to work an environment file specifying the related kafka and mongo servers is needed. While a default file ('hop_comms/auxiliary/test-config.env') comes with the package, it can also be set from the command line on-flight.  

Below, we present a quick start for the Supernova Early Warning System communication tools [Python API](#Python-Api) using both [Jupyter Notebooks](#snews-on-jupyter-notebooks), and also the [command line interface](#command-line-interface)(CLI).

While can be called from terminal using a CLI, the package also allows jupyter notebook interactions as described in [Python API](#Python-Api)

**Table of Contents**
1. [SNEWS on Jupyter Notebooks](#python-api)
    1. [Subscribe](#subscribing-to-a-topic)
    2. [Publish](#publishing-to-a-topic)
    
2. [Command Line Interface-(CLI)](#command-line-interface)
    1. [Subscribe](#subscribe)
    2. [Publish](#publish)
    3. [Publish Heartbeat](#publish-heartbeat)
    4. [Coincidence Decider](#coincidence-decider)
    5. [Simulate Observation](#simulation)
    6. [Retraction](#retract)


## Python-Api
The hop_comms modules are IPython friendly and can be executed in jupyter notebook environments. However, in order to execute different cells asynchronously, one need to invoke `ipyparallel` first. For this, launch a new linux terminal and eun the following commands;
```bash
conda install ipyparallel
ipcluster nbextension enable -n 2
ipcluster start -n 2
```
This enables the relevant notebook extension to executes multiple cells together. After setting this, go back to jupyter notebook and import `ipyparallel` and `hop_comms`.

```python
from ipyparallel import Client
rc = Client()
```

### Subscribing to a topic
To execute different cells together, a _jupyter magic command_ has to be provided in the beginning of each cell
```python
%%px -a -t 0
from hop_comms.hop_sub import HopSubscribe
sub = HopSubscribe()
sub.subscribe()
```

The `hop_comms.hop_sub.HopSubscribe().subscribe()` command subscribes to the **observation** topic that is set by the environment variable by default. The default environment configuration is provided by the package but can also be provided by the user.<br>

```python
from hop_comms.snews_utils import set_env
set_env(<THE PATH TO YOUR CONFIG FILE>)
```

### Publishing to a topic

```python
%%px -a -t 1
from hop_comms.hop_pub import Publish_Tier_Obs
from hop_comms.snews_utils import data_obs

pub = Publish_Tier_Obs()
data = data_obs() # default values 
pub.publish(<EXPERIMENT NAME>, "CoincidenceTier", data)
```

the `snews_utils.data_obs` provides the message template set by `hop_comms.hop_mgs_schema`, all values are default to `None`. 


## Command Line Interface

Once build the program can also be called from the terminal
```bash
hop_comms --help
```
Displays the valid command and options. 

### Subscribe
To simply subscribe to an observation topic that is either already set by the environment variables (i.e. `echo $OBSERVATION_TOPIC` is not `None`), 
```bash
hop_comms subscribe O
```
or to an explicit topic name e.g. "kafka://kafka.scimma.org/snews.experiments-test".
```bash
hop_comms subscribe -b "kafka://kafka.scimma.org/snews.experiments-test"
```
or an environment configuration file can also be given on the fly
```bash
hop_comms subscribe -env "path/to/environment/config/file"
```

One can also subscribe to alert messages using `A` argument instead of `O` in the first example. <br>
_See also_ `hop_comms subscribe --help`


### Publish

To publish messages directly from the terminal, one can simply call
```bash
hop_comms publish
```
In which case the application uses the `'TEST'` detector, and publishes a default dictionary with all values are set to `None` at the time of execution. <br>

The `sent_time` is always set to time of execution. One can provide `--no-bypass` key in which case the user is prompted with a text editor to make adjustments in the dictionary. <br>

**Note:** publishing an observation message from a pre-saved file is not yet implemented. <br>

For other options see
```bash
hop_comms publish --help
```

### Publish Heartbeat
```bash
hop_comms publish_heartbeat
```

### Coincidence Decider
```bash
hop_comms run-coincidence
```

### Simulation

```bash
hop_comms simulate
```
Takes options `-r/--rate` for simulation rate, `-p/--alert_probability` to decide if a simulated observation message will be published or not.

### Retract
```bash
hop_comms retract
```

Notes
-----

- In general, subscription is only possible for the *Alert* topics
- To publish and subscribe user needs necessary kafka credentials.
- For the moment, the coincidence decider needs to be called externally