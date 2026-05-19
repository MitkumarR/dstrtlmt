from prometheus_client import Counter, Histogram, Gauge

requests_total = Counter(
    "ratelimiter_requests_total",
    "Total requests received",
    ["client_key", "status"]   # status: allowed / blocked
)

request_latency = Histogram(
    "ratelimiter_request_duration_seconds",
    "Request processing latency"
)

active_clients = Gauge(
    "ratelimiter_active_clients",
    "Unique clients seen in the last window"
)