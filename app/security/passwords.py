# app/security/passwords.py

from passlib.context import CryptContext
import bcrypt

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper to hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Helper to verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Method to set the hashed password
def set_password(password: str):
    """Set the hashed password"""
    return get_password_hash(password)

# Method to verify the password
def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return verify_password(plain_password, hashed_password)