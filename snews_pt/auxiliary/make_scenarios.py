import json

msg1 = {"detector_name": "XENONnT",
        "neutrino_time": "30/01/01 12:34:45:678999",
        "p_val": 0.98}

msg2 = {"detector_name": "DS-20K",
        "neutrino_time": "30/01/01 12:34:47:678999",
        "p_val": 0.98}

msg3 = {"detector_name": "DUNE",
        "neutrino_time": "30/01/01 12:34:55:678999",
        "p_val": 0.98}

msg4 = {"detector_name": "JUNO",
        "neutrino_time": "30/01/01 12:30:55:678999",
        "p_val": 0.98}

msg5 = {"detector_name": "Baksan",
        "neutrino_time": "30/01/01 12:30:52:678999",
        "p_val": 0.98}

msg6 = {"detector_name": "JUNO",
        "neutrino_time": "30/01/01 12:30:56:678999",
        "p_val": 0.98}

####
msg7 = {"detector_name": "Borexino",
        "neutrino_time": "30/01/01 12:30:10:678999",
        "p_val": 0.98}

msg8 = {"detector_name": "ICE",
        "neutrino_time": "30/01/01 12:30:19:678999",
        "p_val": 0.98}

msg9 = {"detector_name": "NOvA",
        "neutrino_time": "30/01/01 12:30:21:678999",
        "p_val": 0.98}

msg10 = {"detector_name": "DS-20K",
        "neutrino_time": "30/01/01 12:30:22:678999",
        "p_val": 0.98}

msg11 = {"detector_name": "HALO",
        "neutrino_time": "30/01/01 12:30:20:678999",
        "p_val": 0.98}

msg12 = {"detector_name": "XENONnT",
        "neutrino_time": "30/01/01 12:30:29:678999",
        "p_val": 0.98}

msg13 = {"detector_name": "JUNO",
        "neutrino_time": "30/01/01 12:30:18:678999",
        "p_val": 0.98}


scenarios = {
    "simple coincidence": [msg1,msg2],
    "exact 10s coincidence": [msg1, msg3],
    "two coincidences":[msg1,msg2, msg4, msg5],
    "same message submitted twice":[msg1, msg1],
    "same detector submits within 1sec":[msg4, msg6],
    "3 coincident message, out of order":[msg3, msg2, msg1],
    "msgs at 10, 19, 21, 22, 20, 29, 18 seconds": [msg7,msg8,msg9,msg10,msg11,msg12,msg13],
}

with open("scenarios.json", "w") as write_file:
    json.dump(scenarios, write_file, indent=2)