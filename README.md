# SNEWS Publishing Tool

This packages provides users with a Python API and CLI to publish observation messages to SNEWS

    Note: CLI is still WIP 

## How to Install

    Note: Make sure your hop credentials are set up !!

First you need to clone this repo. In your terminal run the following:

````bash 
git clone https://github.com/SNEWS2/SNEWS_Publishing_Tools.git
````

Once cloned, install the package using pip (make sure you're in the cloned dir)

````bash
pip install .
````

## Message Schemas

    Note: Not the final schemas !!

### Coincidence Tier

````
_id                 
detector_name     (user input)    
sent_time           
machine_time      (user input)    
neutrino_time     (user input)     
p_value           (user input)    
````

### Significance Tier

````
_id                 
detector_name    (user input)      
sent_time           
machine_time     (user input)        
neutrino_time    (user input)       
p_value(s)       (user input)    
````

### Time Series Tier

````
_id                
detector_name   (user input)      
sent_time           
machine_time    (user input)      
neutrino_time   (user input)     
timing_series   (user input)
````

### False Obs

````
_id
detector_name           (user input)          
false_id                (user input, optional)    
which_tier              (user input)    
N_retract_latest        (user input)    
retraction_reason       (user input, optional)  
sent_time           
````

## How to Publish

Before we get started, right now the publishing method will send your message to the test kafka server.

First you need to import Publisher and  your desired Observation class:

````Python
# Import the Publisher class
from SNEWS_PT.snews_pub import Publisher
# Import the constructor for Coincidence Tier
from SNEWS_PT.snews_pub import CoincidenceTier
# Import the constructor for Significance Tier
from SNEWS_PT.snews_pub import SignificanceTier
# Import the constructor for Timing Tier
from SNEWS_PT.snews_pub import TimingTier
````

First let's make a dummy nu time method (optional)

    Note: datetime object will be used to create a dummy nu times

```Python
from datetime import datetime


def nu_t():
    return datetime.utcnow().strftime("%H:%M:%S:%f")
```

Let's define the name of our detector.
```Python
my_detector = 'DS-20K'

```


Finally, to send a message you need initialize the Publisher, construct your message, and send it to Publisher. 
```Python
with Publisher() as pub:
    message = CoincidenceTier(detector_name=my_detector, , neutrino_time=nu_t(), p_value = 0.98,).message()
    pub.send(message)
```

The output should look like this:
![img.png](img.png)

See `example.ipynb` for more tutorial scripts 

## How to Subscribe

In two lines, one can subscribe to the alert topic specified in the default configuration. <br>
This starts a stream, and waits for alert messages to be received.
```python
from SNEWS_PT.snews_sub import Subscriber

Subscriber().subscribe()
```

---
# Command Line Interface (CLI)
All the commands have their short descriptions accesible via `--help` flag. 
```bash
(venv) User$: snews_pt --help 
```
```bash
  User interface for snews_pt tools 
  Options:
   --version   Show the version and exit. 
   --env TEXT  environment file containing the configurations  
               [default:(auxiliary/test-config.env)]
   --help      Show this message and exit.
  
  Commands:
   hearbeat 
   message-schema  Display the message format for `tier`, default 'all'
   publish         Publish a message using snews_pub
   retract 
   subscribe       maybe also implement context menager
```

Currently, the `retract` and `heartbeat` methods are not implemented in the CLI. All other commands can be called from the terminal. See their help for instructions.
Quick demonstration;
```bash 
(venv) User$: snews_pt subscribe 
> You are subscribing to ALERT                                                                                            
> Broker:kafka://kafka.scimma.org/snews.alert-test
```
by default subscribes to the `ALERT_TOPIC` specified in the default environment file. This environment file can be modified, or a different one can be passed.

Publishing method have several aliases for `coincidence`, `significance`, `timing`, `heartbeat` and `retraction`. Currently, the last two will raise a `NotImplementedError`, and planned to be added soon.
The rest of the publishing methods can take either a `.json` file saved in the local machine, or for test purposes, submit a default message.
**Notice that all the tiers have their expected message schemes** these schemes can be seen by;

```bash
(venv) User$: snews_pt message-schema
```
by default this display the message schema for all tiers, and specifies which fields can be set by the user.
Finally, to submit a message;
```bash
(venv) User$: snews_pt publihs C t FalSe hB
```
notice that here we are publishing a default message that is structured with respect to its own tier. Also notice that there can be several case insensitive aliases for the tiers i.e. `C`, `c`, `coinc`, `coinCiDence`, `coincidencetier` would all publish to the same tier.
