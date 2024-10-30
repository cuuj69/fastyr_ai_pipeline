from prometheus_client import Counter, Histogram
from functools import wraps
import time

# Define metrics
REQUEST_COUNT = Counter(
    'fastyr_request_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'fastyr_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

def track_metrics(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            response = await func(*args, **kwargs)
            REQUEST_COUNT.labels(
                method=args[0].method,
                endpoint=args[0].url.path,
                status=response.status_code
            ).inc()
            return response
        finally:
            REQUEST_LATENCY.labels(
                method=args[0].method,
                endpoint=args[0].url.path
            ).observe(time.time() - start_time)
    return wrapper 