# SNEWS Publishing Tool
This packages provides users with a Python API and CLI to publish observation messages to SNEWS 


    Note: CLI is still WIP 


## How to Install
    Note: Make sure your hop credentials are set up !!

First you need to clone this repo. In your terminal run the following: 

````bash 
git clone https://github.com/SNEWS2/SNEWS_PT.git
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

First you need to import the Publish_Tier_Obs class and the data_obs method:
````Python
from SNEWS_PT.hop_pub import Publish_Tier_Obs
from SNEWS_PT.snews_pt_utils import data_obs
from datetime import datetime
````
    Note: datetime object will be used to create a dummy nu times

Initialize Publish_Tier_Obs
````Python
pub = Publish_Tier_Obs()
````

Make your dummy nu time method (optional)
```Python
def nu_t():
    return datetime.utcnow().strftime("%H:%M:%S:%f")
```

Set detector name
````Python
my_detector = 'DS-20K'
````

Now set fill data_obs with your data and publish it !!
```Python
data = data_obs(p_value=0.6,nu_time=nu_t())
pub.publish(my_detector, 'CoincidenceTier', data)
```