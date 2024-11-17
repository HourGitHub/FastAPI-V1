# app/utility/verify_token.py

import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Optional

# Secret key and algorithm for JWT (make sure to store this securely in your environment)
SECRET_KEY = os.getenv("SECRET_KEY", "4y$Wz!7Jm^rT2k$Qh&b9@Fz2mW3n#E1p")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Adjust based on your needs

# Define the exception for expired or invalid tokens
class TokenError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

# Verify the JWT token and extract user information
def verify_token(token: str) -> Optional[int]:
    """
    Verifies the token and extracts the user ID if valid.
    
    :param token: The JWT token to verify.
    :return: User ID if token is valid, otherwise raises an exception.
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if the token has the 'sub' field which typically holds the user_id
        user_id = payload.get("sub")
        if user_id is None:
            raise TokenError("Token doesn't contain user information.")
        
        # Return the user ID from the token
        return int(user_id)  # Assuming user_id is stored as integer in 'sub'
    
    except JWTError:
        raise TokenError("Invalid token or expired token.")
    except Exception as e:
        raise TokenError(f"Token verification failed: {str(e)}")

# Example to create a new token (for your reference)
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT token with user data.
    
    :param data: The user data to include in the token (e.g., user_id).
    :param expires_delta: How long the token should be valid for.
    :return: The JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
