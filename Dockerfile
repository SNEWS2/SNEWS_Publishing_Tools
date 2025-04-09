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

#RUN apt-get update && apt-get install -y --no-install-recommends git build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

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
