import json
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

data = json.load(open(sys.argv[1]))

logging.info("Reading alert data and running the firedrill plugin script")
logging.info("Here is the alert dictionary I received:")
for k, v in data.items():
    logging.info(f"{k:20s} : {v}")