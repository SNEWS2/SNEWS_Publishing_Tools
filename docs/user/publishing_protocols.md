# Publishing Protocols

Users from certain experiments can send their observations to SNEWS for creating a coincidence with the other incoming messages. 
These "observation messages" are not public unless they coincide with another observation message from another experiment within 10 seconds. 
In which case the SNEWS server triggers a "coincidence alert message" to all of its subsribers.

Members can share information about their observation. Based on the scope of shared information different tiers can work on different aspects. 


The most basic information a detector can share is the initial neutrino time of their observation. 
This information is used to form a **Coincidence** with other initial neutrino times acquired from other detectors. 
The coincidences are handled within the **"Coincidence Tier"** and by the [SNEWS Coincidence System](https://github.com/SNEWS2/SNEWS_Coincidence_System).

If further information is shared e.g. combined sensitivities can be computed (**"Significance Tier"**) by using the individual neutrino events, or 
the location of the supernova can be triangulated (**"Time Tier"**).

The user can share as much information as they desire with one simple function call. The predetermined fields 
sets the "Tier" and any additional information is passed under `meta` field.

The user can use `SNEWSTiersPublisher` to create observation message(s) and send them to snews.
```python
from snews_pt.snews_pub import SNEWSTiersPublisher
messages = SNEWSTiersPublisher(neutrino_time="2022-02-28T04:31:08.678999")
messages.send_to_snews()
```
User can also investigate their messages before sending it to SNEWS. The `SNEWSTiersPublisher` creates an object which contains 
the generated and formatted messages. It can also tell you what "Tiers" are selected based on the input that is given. 

The example above shows the minimal working example. Assuming that the detector name has already been set by `snews_pt.snews_pt_utils.set_name()` function
only passing the neutrino time in ISO-format creates a message for the Coincidence Tier which can be sent to snews easily. 
Similarly, if you have a JSON file that contains the same information in the correct format, this can also be passed to snews using command line interface;
```bash
snews_pt publish myjsonfile.json
```

### Things to note

For your messages to pass your name has to be set. If you haven't done so, `snews_pt` will raise a warning. 
Unless you are sending messages with a known name they will not be read by the server.

Similarly, the times are always in ISO-format (``"%Y-%m-%dT%H:%M:%S.%f"``) otherwise, the tools will raise an error.

If you are testing, you need to pass the argument `is_test=True` otherwise, the messages that contain a neutrino time that 
is not within the last 48 hours will be rejected. Testing allows setting times in the future or from past.

The server runs a specific kafka topic, some topics (e.g. "OBSERVATION_TOPIC", "ALERT_TOPIC", "FIREDRILL_TOPIC") are set 
on the environment file by default. The `snews_pt` tools can read these, but you can tell it whether you want to use the 
firedrill topic or not by passing `firedrill_mode=True` or `firedrill_mode=False` based on which it selects either of the topics.


### Tier Decider
There is a `tier_decider` module that decides and generates different messages with the SNEWS format based on the input you pass.
> if you pass `neutrino_time` the Publisher labels it as "Coincidence Tier" <br>
> if you pass `p_values` and `t_bin_width` it is labeled as "Significance Tier Message" <br>
> if you pass `timing_series` it is labeled as "Time Tier" <br>
> if you pass `retract_latest` (e.g. retract_latest=1 retracts the last 1 message) it labels as "Retraction Message" <br>
> if you pass `detector_status` it labels as "Heartbeat Message" (Notice HB doesn't require time as it stamps itself) <br>


**Coincidence Tier**

* ``neutrino_time`` need to be passed.
    * ``neutrino_time`` must be a ``string`` with ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

**Significance Tier**

* ``p_values`` needs to be passed.
    * ``p_values`` must be a ``list (float)``.

**Timing Tier**

* ``p_value`` and ``timing_series`` need to be passed.
    * ``p_val`` must be a ``float``.
    * ``timing_series`` must be a ``list (string)``, ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

**Retraction**

* ``retract_latest`` need to be passed.
    * ``retract_latest`` must be a ``int (and >0 )``. 

**Pre-SN Timing Tier**

* ``is_pre_sn`` and ``timing_series`` need to be passed.
    * ``is_pre_sn`` must be a ``bool``.
    * ``timing_series`` must be a ``list (string)``, ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

Notice that your message can contain fields that correspond to several tiers e.g. if you have ``p_value``, ``neutrino_time``, and ``p_values`` we submit two separate messages to _Coincidence_ and _Significance_ tiers by selecting the relevant fields from your input.


#### Example;

In the example below `SNEWSTierPublisher` creates a message for "CoincidenceTier" because the `neutrino_time` is passed, and it creates 
another message for the "Significance Tier" because the `p_values` together with the `t_bin_width` is passed. 

Here the `p_val` is the p value of the detection and it is optional. The `detector_name` can be passed manually, however, if the name is initially set, this is also not needed.

<img src="../example_publishing.png" alt="Publication example" width="2000"/>


