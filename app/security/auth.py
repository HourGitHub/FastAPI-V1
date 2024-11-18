# app/security/auth.py
import logging
import os
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.db.models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext  # For password hashing
from fastapi_jwt_auth import AuthJWT  # For JWT handling
from datetime import timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ensure SECRET_KEY is loaded from environment
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SECRET_KEY not set in environment variables")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # Default to 15 minutes if not set

    class Config:
        env_file = ".env"


@AuthJWT.load_config
def get_config() -> Settings:
    """Load JWT configuration settings."""
    return Settings()


def get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)) -> User:
    try:
        Authorize.jwt_required()
        user_email = Authorize.get_jwt_subject()
    except Exception as e:
        logging.error(f"JWT validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed")

    user = db.query(User).filter(User.email == user_email).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user



def create_access_token(subject: str, expires_delta: int = None, Authorize: AuthJWT = Depends()) -> str:
    """Generate an access JWT token."""
    expiration = timedelta(minutes=expires_delta) if expires_delta else timedelta(minutes=Settings.authjwt_access_token_expires)
    return Authorize.create_access_token(subject=subject, expires_time=expiration)


def create_refresh_token(subject: str, Authorize: AuthJWT = Depends()) -> str:
    """Generate a refresh JWT token."""
    return Authorize.create_refresh_token(subject=subject)


# Optional: Custom exception handler can be added for JWT errors, useful for global error handling.
def handle_invalid_token_error():
    """Handle invalid token error globally."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token or token has expired."
    )



def verify_refresh_token(refresh_token: str):
    # Your logic to verify refresh token here
    pass  # Replace this with the actual implementation
