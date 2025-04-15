#!/bin/bash
#set -e

# Make test messages and start containers
#docker compose up -d --build --force-recreate
docker compose build --build-arg HOP_USERNAME=${HOP_USERNAME} --build-arg HOP_PASSWORD=${HOP_PASSWORD}
docker compose up -d --force-recreate

echo "Waiting for containers to be ready..."
sleep 3

# Publish messages
docker exec publishing_tools_publisher snews_pt publish /app/snews_pt/test/firedrill_combined_message.json --firedrill
docker exec publishing_tools_publisher snews_pt publish /app/snews_pt/test/firedrill_combined_message2.json --firedrill

echo "Messages published."