from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.limiter import is_allowed
from app.metrics import requests_total, request_latency, active_clients
import time

app = FastAPI(title="Distributed Rate Limiter")

def get_client_key(request: Request) -> str:
    # Use X-API-Key header if present, fall back to IP
    return request.headers.get("X-API-Key") or request.client.host

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip middleware for /metrics and /health
    if request.url.path in ("/metrics", "/health"):
        return await call_next(request)

    client_key = get_client_key(request)
    start = time.time()

    allowed, current, remaining = await is_allowed(client_key)

    status = "allowed" if allowed else "blocked"
    requests_total.labels(client_key=client_key, status=status).inc()
    request_latency.observe(time.time() - start)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "retry_after": 60},
            headers={
                "X-RateLimit-Limit": str(10),
                "X-RateLimit-Remaining": "0",
                "Retry-After": "60"
            }
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Current"] = str(current)
    return response

@app.get("/")
async def root():
    return {"message": "Hello from the rate-limited API"}

@app.get("/data")
async def get_data():
    return {"data": [1, 2, 3, 4, 5]}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "ok"}