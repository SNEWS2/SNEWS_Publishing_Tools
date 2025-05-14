FROM python:3.11-bullseye

WORKDIR /app

COPY . .

SHELL ["/bin/bash", "-c"]

# Accept build arguments
ARG HOP_USERNAME
ARG HOP_PASSWORD

# Set environment variables
ENV HOP_USERNAME=${HOP_USERNAME}
ENV HOP_PASSWORD=${HOP_PASSWORD}

# Set observation and alert topics for github CI firedrill
RUN sed -i 's/^FIREDRILL_OBSERVATION_TOPIC=.*/FIREDRILL_OBSERVATION_TOPIC=kafka:\/\/$\{HOP_BROKER\}\/snews\.experiments-github/' /app/snews_pt/auxiliary/test-config.env
RUN sed -i 's/^FIREDRILL_ALERT_TOPIC=.*/FIREDRILL_ALERT_TOPIC=kafka:\/\/$\{HOP_BROKER\}\/snews\.alert-github/' /app/snews_pt/auxiliary/test-config.env

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

RUN chmod +x /app/generate_firedrill_creds.sh
RUN /app/generate_firedrill_creds.sh

# Install the project
RUN pip install .
RUN hop auth add hop_creds.csv
RUN mkdir -p /app/output
RUN snews_pt set-name -n JUNO

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
