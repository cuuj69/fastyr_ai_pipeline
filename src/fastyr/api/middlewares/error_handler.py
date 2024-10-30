from fastapi import Request
from fastapi.responses import JSONResponse
from fastyr.core.exceptions import FastyrException
import sentry_sdk

async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except FastyrException as e:
        sentry_sdk.capture_exception(e)
        return JSONResponse(
            status_code=400,
            content={"code": e.code, "message": e.message}
        )
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JSONResponse(
            status_code=500,
            content={"code": "INT_001", "message": "Internal server error"}
        ) 