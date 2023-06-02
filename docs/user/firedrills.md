

# Firedrills

SNEWS conducts occasional firedrills to different extends. 
The idea is to simulate a realistic chain of events that we expect to happen once we start detecting a signal from a supernova.
This starts with the communication between detectors and the SNEWS servers, and continues with individual tasks of 
different tiers such as coincidence detection, triangulation, latency calculations, and follow up integrations. <br>

SNEWS has successfully tested the communication using `snews_pt` and `snews_cs` and frequently challenges the code.

Current firedrills focusses on making sure that every member detector can communicate their messages from their machines 
and ready to receive alerts, as well as testing the snews coincidence server. 

More elaborate firedrills including extracting statistical information based on the active detectors by tracking the heartbeats, 
selecting a candidate star and computing the time delays from such star to add as delays to the detectors, and trying to triangulate are work in progress.

----

## To Do's for the Detectors
First, please follow the [Installation Guide](https://snews-publishing-tools.readthedocs.io/en/latest/user/installation.html) and 
[**Quick Start**](https://snews-publishing-tools.readthedocs.io/en/latest/user/quickstart.html)

In order to participate in the firedrills, the detectors should have the latest version of the publishing tools `snews_pt`.

Each user have the option to use either the API or the CLI tools to interact with the server. 

We would like to test two main interactions; **subscribing**  & **publishing** to snews.


### Subscribe

- API:
    ```python
     from snews_pt.snews_sub import Subscriber
     Subscriber().subscribe()
    ```
- CLI
   ```bash
  user/home$: snews_pt subscribe
   ```

### Publish

- API:
    ```python
     from snews_pt.snews_pub import SNEWSTiersPublisher
     SNEWSTiersPublisher(detector_name='KamLAND', 
                         neutrino_time="2022-02-28T04:31:08.678999",
                         p_val=0.000007,
                         machine_time="2022-02-28T04:31:09.778859", 
                         firedrill_mode=True,
                         is_test=True,
                         ).send_to_snews()
    ```
  or 
  ```python
  from snews_pt.snews_pub import SNEWSTiersPublisher
  observation = SNEWSTiersPublisher.from_json('somejsonfile.json', 
                                              detector_name='XENONnT',
                                              firedrill_mode=True,
                                              is_test=True, 
                                              comment="This is submitted from a json file")
  observation.send_to_snews()
  ```
Notice that `SNEWSTiersPublisher` returns an object which actually contains the decided tiers, and formatted messages. 
One can play with this object before finally `send_to_snews()`.  

- CLI
   ```bash
  user/home$: snews_pt publish --firedrill myjsonfile.json
   ```


-----

## Notes:
### Subscribe and Redirect

`snews_pt subscribe` also allows for other scripts to be plugged in and act on alerts. The *CLI* command `snews_pt subscribe` takes the custom made script via `--plugin` (`-p`) option.

```bash 
user/home$: snews_pt subscribe --firedrills -p custom_made_script.py
```

`snews_pt subscribe` saves the alert messages to a local JSON file with the date stamp of the received time. When a custom plugin is provided, as soon as an alert is received and JSON is created, the name of this unique-JSON file is passed to the script and executed.

Therefore, all custom-made scripts should contain the following two lines;

```python
# in "custom_made_script.py"
import sys, json
data = json.load(open(sys.argv[1]))
```
and do the follow-up work using the `data` dictionary as the alert message. See [this dummy example](https://github.com/SNEWS2/SNEWS_Publishing_Tools/blob/main/snews_pt/test/random_plugin.py).


### On the first run

The publishing tools will want to know the user. To aid the user, instead of asking for a user name, we developed a method to
set the user-name only one time. By default `snews_pt` assigns you the name `"TEST"` and as long as you do not change this, it raises an error message.

This name can easily be set by API or CLI
- API
```python
    import snews_pt
    snews_pt.snews_pt_utils.set_name("NAMEOFDETECTOR")
```

- CLI
```bash
    user/home$: snews_pt set-name --name NAMEOFDETECTOR
```
















