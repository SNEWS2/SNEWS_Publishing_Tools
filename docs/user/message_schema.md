
# Message Schemas

Each observation tier and respectively the retraction messages follow a certain structure. <br>
In the next releases any additional json-serializable key-value pair will be passed as a meta-data, currently 
the tools will raise a `KeyValueError`.

Also notice any message scheme can also be displayed using command line tools;
```bash
(venv) User$: snews_pt message-schema
```
By default this command displays the schemes shown below, individual tier content can also be displayed by typing the 
name of the requested tier e.g. `snews_pt message-schema coincidence` 

    Note: Not the final schemas !!

## Coincidence Tier

````
_id                 
detector_name     (user input)    
sent_time           
machine_time      (user input)    
neutrino_time     (user input)     
p_value           (user input)    
````

## Significance Tier

````
_id                 
detector_name    (user input)      
sent_time           
machine_time     (user input)        
neutrino_time    (user input)       
p_value(s)       (user input)    
````

## Time Series Tier

````
_id                
detector_name   (user input)      
sent_time           
machine_time    (user input)      
neutrino_time   (user input)     
timing_series   (user input)
````

## False Obs

````
_id
detector_name           (user input)          
false_id                (user input, optional)    
which_tier              (user input)    
N_retract_latest        (user input)    
retraction_reason       (user input, optional)  
sent_time           
````
