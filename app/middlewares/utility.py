# app/middlewares/utility.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ExampleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pre-processing the request
        response = await call_next(request)
        # Post-processing the response
        return response
