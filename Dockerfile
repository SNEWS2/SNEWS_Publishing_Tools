FROM python:3.11-bullseye

WORKDIR /app

COPY . .

SHELL ["/bin/bash", "-c"]

#RUN apt-get update && apt-get install -y --no-install-recommends git build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install hop -r requirements.txt

# Install the project
RUN pip install .
RUN hop auth add hop_creds.csv
RUN mkdir -p /app/output
RUN snews_pt set-name -n JUNO

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]
