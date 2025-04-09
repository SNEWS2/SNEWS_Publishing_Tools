import json
import os
from datetime import datetime, timedelta


def write_data(filename, detector_name, current_time):
    # Create the JSON data with current time values
    data = {
        "detector_name": detector_name,
        "machine_time": current_time.isoformat(),
        "neutrino_time_utc": (current_time - timedelta(seconds=7)).isoformat(),
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

    # Save the JSON data to the specified file
    with open(filename, 'w') as file:
        file.write(json_data)


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define filenames relative to the script directory
    file1 = os.path.join(script_dir, 'firedrill_combined_message.json')
    file2 = os.path.join(script_dir, 'firedrill_combined_message2.json')

    # Write data to the files
    write_data(file1, 'XENONnT', datetime.utcnow())
    write_data(file2, 'JUNO', datetime.utcnow())
