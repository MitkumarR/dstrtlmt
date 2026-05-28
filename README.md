# Distributed Rate Limiter

A scalable, distributed rate-limiting API built with FastAPI and Redis, complete with built-in observability using Prometheus and Grafana.

## Architecture

This project is built using a modern microservices stack and orchestrated with Docker Compose:

- **FastAPI**: The core web framework serving the API.
- **Redis**: The centralized, in-memory data store used to share rate-limiting state across multiple API replicas.
- **Prometheus**: A time-series database configured to continuously scrape request metrics (allowed vs. blocked) from the API.
- **Grafana**: A visualization layer connected to Prometheus for building real-time dashboards of API traffic and rate-limit events.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quickstart

1. **Clone the repository** (if you haven't already) and navigate to the project directory:
   ```bash
   cd dstrtlmt
   ```

2. **Start the infrastructure**:
   ```bash
   sudo docker compose up -d
   ```
   *Note: This spins up 2 replicas of the API, along with Redis, Prometheus, and Grafana.*

3. **Verify the services are running**:
   ```bash
   sudo docker ps
   ```
   You should see 5 containers running. The API replicas will be bound to host ports `8000` and `8001`.

## Testing the Rate Limiter

The application is configured to limit requests (e.g., 10 requests per 60 seconds per client). Because the state is stored in Redis, the limit is strictly enforced regardless of which API replica receives the request.

You can simulate traffic and trigger the rate limit by running this simple bash loop:

```bash
for i in {1..15}; do curl -s http://localhost:8000/ > /dev/null; echo "Request $i sent"; done
```
You should notice that after the configured limit is reached, the API will start returning `429 Too Many Requests` or a blocked response.

## Observability & Monitoring

The API exposes metrics at the `/metrics` endpoint. 

### Prometheus
- **URL**: [http://localhost:9090](http://localhost:9090)
- You can query raw metrics here. Try searching for `requests_total` to see the raw counts of allowed and blocked requests.

### Grafana
- **URL**: [http://localhost:3000](http://localhost:3000)
- **Login**: `admin` / `admin` (Configured via `docker-compose.yml`)
- **Setup**: 
  1. Add a new **Prometheus** Data Source.
  2. Set the connection URL to `http://prometheus:9090`.
  3. Create a Dashboard and add a visualization using the `requests_total` metric to see your rate limiting in action!
