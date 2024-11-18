# app/middlewares/auth.py

import logging
from fastapi import HTTPException, Request

from app.security.auth import get_current_user

# Middleware to check token validity
async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=403, detail="Token is missing")
    
    try:
        current_user = get_current_user(token)
        request.state.user = current_user
    except Exception as e:
        # Log the exception
        logging.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=403, detail="Token is invalid")
    return request
