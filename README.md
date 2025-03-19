# Streamlit Service (a.k.a streamlit-ui)

This repository contains a Dockerized Streamlit service that provides an interactive web-based UI.

## Features
- Runs a Streamlit app inside a Docker container
- Easily configurable via environment variables
- Supports deployment with Docker Compose

## Requirements
- Docker

## Environment Variables
The following environment variables can be set:

| Variable       | Description                                  | Default            |
|----------------|----------------------------------------------|--------------------|
| `API_BASE_URL` | Port on which the Streamlit app runs         | `http://localhost` |
| `API_TOKEN`    | Token to authentificate against backend API  | None               |

[All needed environment variables can copied from the file.](.env.example)
## Usage

### Build and Run with Docker
```sh
# Build the Docker image
docker build -t streamlit-ui .

# Run the container
docker run -d \
  -p 8501:8501 \
  --env API_BASE_URL=http://localhost:8000 \
  --env API_TOKEN=awesome-api-token \
  streamlit-ui
```

### Docker Compose
To deploy with Docker Compose, create a `docker-compose.yml` file:

```yaml
version: '3'
services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://localhost:8000
    depends_on:
      - backend
```

Run the service:
```sh
docker-compose up -d
```

## Logs and Monitoring
To check logs:
```sh
docker logs -f streamlit-ui
```

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.
