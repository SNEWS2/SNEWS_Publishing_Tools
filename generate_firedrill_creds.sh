#!/bin/bash

# Check if the required environment variables are set
if [[ -z "$HOP_USERNAME" || -z "$HOP_PASSWORD" ]]; then
  echo "Error: HOP_USERNAME and HOP_PASSWORD environment variables must be set."
  exit 1
fi

# Create the hop_creds.csv file
echo "username,password" > /app/hop_creds.csv
echo "$HOP_USERNAME,$HOP_PASSWORD" >> /app/hop_creds.csv

echo "hop_creds.csv file created successfully."
