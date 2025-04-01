import json
from datetime import datetime, timedelta


def write_data(filename, detector_name, current_time):
    # Create the JSON data with current time values
    data = {
        "detector_name": detector_name,
        "machine_time": current_time.isoformat(),
        "neutrino_time": (current_time - timedelta(seconds=7)).isoformat(),
        "timing_series": [
            (current_time - timedelta(seconds=7)).isoformat(),
            (current_time - timedelta(seconds=6.7)).isoformat(),
            (current_time - timedelta(seconds=6.3)).isoformat()
        ],
        "detector_status": "ON",
        "p_val": 0.05,
        "p_values": [0.4, 0.5, 0.09, 0.04],
        "t_bin_width": 0.6,
        "is_test": "False"
    }

    # Convert the data to a JSON string
    json_data = json.dumps(data, indent=4)

    # Save the JSON data to two different files
    with open(filename, 'w') as file1:
        file1.write(json_data)



if __name__ == "__main__":

    write_data('snews_pt/test/firedrill_combined_message.json', 'XENONnT', datetime.utcnow())
    write_data('snews_pt/test/firedrill_combined_message2.json', 'JUNO', datetime.utcnow())