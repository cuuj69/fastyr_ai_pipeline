from fastapi import Request, HTTPException
from fastyr.core.contracts.constants import ErrorCodes
import time
from collections import defaultdict
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        
    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < 60
        ]
        
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail={"code": ErrorCodes.RATE_LIMITED, "message": "Too many requests"}
            )
            
        self.requests[client_ip].append(now) 