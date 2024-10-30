from functools import wraps
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integratgions.sqlalchemy import SqlalchemyIntegration
from fastyr.core.contracts.constants import API_VERSION

def init_sentry(dsn:str):
    """Initialize Sentry monitoring."""
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0,
        release=API_VERSION,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ]
    )

def monitor_task(func):
    """Decorator to monitor async tasks with Sentry."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        with sentry_sdk.start_transaction(op="task", name=func.__name__):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                sentry_sdk.capture_exception(e)
                raise
    return wrapper
