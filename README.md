# SNEWS Publishing Tool

[![Documentation Status](https://readthedocs.org/projects/snews-publishing-tools/badge/?version=latest)](https://snews-publishing-tools.readthedocs.io/en/latest/?badge=latest)
![testing](https://github.com/SNEWS2/SNEWS_Publishing_Tools/actions/workflows/ubuntu20-py39.yml/badge.svg)
<br>See the docs at

|              |        |
| ------------ | ------ |
| **Docs:**    | https://snews-publishing-tools.readthedocs.io/en/latest/  |

This packages provides users with a Python API and CLI to publish observation messages to SNEWS

## How to Install

> Note: Make sure your hop credentials are set up !!<br>
> Follow the instructions [**here**](https://github.com/scimma/hop-client) if needed

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
p_val             (user input)    
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

First you need to import your Publisher:

````Python
# Import the constructor for SNEWS Tiers and Publisher class
from SNEWS_PT.snews_pub import SNEWSTiersPublisher
````
### Passing Message Parameters as Arguments. 
To send a message you need initialize the ``Publisher``, construct your message by initializing ``SNEWSTiers`` and
passing your parameters of choice. The backend will parse your arguments, check their data types and determine which
tiers you can send a message to (see **Publishing Protocols**). If you pass multiple parameters (_see code bellow_) the
sender will send a message *all* the appropriate tiers.

```Python

SNEWSTiersPublisher(detector_name='KamLAND', neutrino_time='22/02/28 4:31:08:565',
                    timing_series=['22/02/28 4:31:08:565', '22/02/28 4:31:08:765', '22/02/28 4:31:09:001'],
                    p_val=0.000007, machine_time='22/02/28 4:31:08:565', 
                    ).send_to_snews()
```

This instance has parameters for **CoincidenceTier** and **TimingTier**, thus it will send a message to both. The output
should look like this:
![img.png](img.png)!


### Passing Message Parameters from JSON File.

You can also pass your input from a json file, and make modifications on the spot. Let's first create an `observation` object this time before sending it to snews;

```
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

### Publishing Protocols

**Coincidence Tier**

* ``p_value`` and ``neutrino_time`` need to be passed.
    * ``p_val`` must be a ``float``.
    * ``neutrino_time`` must be a ``string``, format: ``'%y/%m/%d %H:%M:%S'``

**Significance Tier**

* ``p_values`` needs to be passed.
    * ``p_values`` must be a ``list (float)``.

**Timing Tier**

* ``p_value`` and ``timing_series`` need to be passed.
    * ``p_val`` must be a ``float``.
    * ``timing_series`` must be a ``list (string)``, format: ``'%y/%m/%d %H:%M:%S'``

**Retraction**

* ``n_retract_latest`` and ``which`` need to be passed.
    * ``n_retract_latest`` must be a ``int (and >0 )``. You can also pass it as a ``'ALL'``.
    * ``which_tier`` must be a ``which_tier``, format: ``'%y/%m/%d %H:%M:%S'``

**Pre-SN Timing Tier**

* ``is_pre_sn`` and ``timing_series`` need to be passed.
    * ``is_pre_sn`` must be a ``bool``.
    * ``timing_series`` must be a ``list (string)``, format: ``'%y/%m/%d %H:%M:%S'``

Notice that your message can contain fields that corresponds to several tiers e.g. if you have ``p_value``, ``neutrino_time``, and ``p_values`` we submit two separate messages to _Coincidence_ and _Significance_ tiers by selecting the relevant fields from your input.

## How to Subscribe

In two lines, one can subscribe to the alert topic specified in the default configuration. <br>
This starts a stream, and waits for alert messages to be received.

```python
from SNEWS_PT.snews_sub import Subscriber

Subscriber().subscribe()
```

Should there be an alert message, this will be both displayed on the screen and saved into your local machine
as `SNEWS_MSGs/<today fmt="%y_%m_%d">/subscribed_messages.json` and if there are multiple messages in the same day e.g.
hype-mode is on and for the same supernova you kept receiving alerts with every coincidence message, these will be
appended in this file with the sent time as the first key. An example (partly missing) can be
found [here](https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/doc/subscribed_messages.json)

---

# [Command Line Interface (CLI)](./doc/cli_docs.md)

There also exists tools for command line interactions. These are explained in detail [here](./doc/cli_docs.md)
