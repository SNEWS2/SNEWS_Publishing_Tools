import json

msg1 = {"detector_name": "XENONnT",
        "neutrino_time": "22/01/01 12:34:45:678999",
        "p_value": 0.98}

msg2 = {"detector_name": "DS-20K",
        "neutrino_time": "22/01/01 12:34:47:678999",
        "p_value": 0.98}

msg3 = {"detector_name": "DUNE",
        "neutrino_time": "22/01/01 12:34:55:678999",
        "p_value": 0.98}

msg4 = {"detector_name": "JUNO",
        "neutrino_time": "22/01/01 12:30:55:678999",
        "p_value": 0.98}

msg5 = {"detector_name": "Baksan",
        "neutrino_time": "22/01/01 12:30:52:678999",
        "p_value": 0.98}

msg6 = {"detector_name": "JUNO",
        "neutrino_time": "22/01/01 12:30:56:678999",
        "p_value": 0.98}

scenarios = {
    "simple coincidence": [msg1,msg2],
    "exact 10s coincidence": [msg1, msg3],
    "two coincidences":[msg1,msg2, msg4, msg5],
    "same detector submits twice":[msg1, msg1],
    "same detector submits sequentially":[msg4, msg6],
    "times are out of order":[msg3, msg2, msg1]
}

with open("scenarios.json", "w") as write_file:
    json.dump(scenarios, write_file, indent=2)