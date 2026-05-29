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

# Install snews_pt
RUN pip install --upgrade pip \
    && pip install .

# Generate and add firedrill credentials
RUN chmod +x /app/generate_firedrill_creds.sh
RUN /app/generate_firedrill_creds.sh
RUN hop auth add hop_creds.csv
RUN mkdir -p /app/output
RUN snews_pt set-name -n JUNO

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
