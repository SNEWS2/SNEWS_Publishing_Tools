#!/bin/bash
set -e

#NEED TO FIND A WAY TO GET HOP CREDS INTO THE CONTAINERS AS A CSV
# Set the HOP_AUTH_FILE variable
#export HOP_AUTH_FILE=$(hop auth locate)

# Start docker containers (the docker-compose file will use the exported variables)
python snews_pt/test/generate_firedrill_json.py
docker compose up -d --build --force-recreate

echo "Waiting for containers to be ready..."
sleep 10

# Publish messages
docker exec publishing_tools_publisher snews_pt publish /app/snews_pt/test/firedrill_combined_message.json --firedrill
docker exec publishing_tools_publisher snews_pt publish /app/snews_pt/test/firedrill_combined_message2.json --firedrill

echo "Messages published."