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

First you need to import your desired Publisher class:

````Python
# For Coincidence Tier
from SNEWS_PT.hop_pub import Publisher_Coincidence_Tier
# For Significance Tier
from SNEWS_PT.hop_pub import Publisher_Significance_Tier
# For Timing Tier
from SNEWS_PT.hop_pub import Publisher_Significance_Tier

````


Initialize the Publisher, **make sure you pass it a detector name**! 
    
    Note: For this example I'm publishing to Coincidence Tier.
````Python
my_detector = 'DS-20K'
pub = Publisher_Coincidence_Tier(detector=my_detector)
````

Make your dummy nu time method (optional)

    Note: datetime object will be used to create a dummy nu times
```Python
from datetime import datetime
def nu_t():
    return datetime.utcnow().strftime("%H:%M:%S:%f")
```

Now pass your tier specific data !!
```Python
pub.send_coincidence_tier_message(nu_time=nu_t(), p_value =  0.67)
```

See example for more tutorial scripts 