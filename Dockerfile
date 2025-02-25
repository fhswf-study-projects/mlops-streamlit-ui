FROM python:3.11-slim

WORKDIR /usr/src/app

# Use this space for installing any system dependencies (like curl etc.)
RUN apt-get update -y && \
    apt-get install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*
###

# Install dependencies
RUN pip install poetry
RUN poetry self add poetry-plugin-export

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
###

# OpenTelemetry libraries for monitoring
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-instrumentation-logging \
    opentelemetry-exporter-otlp
###

# Copy project
COPY . .
###
