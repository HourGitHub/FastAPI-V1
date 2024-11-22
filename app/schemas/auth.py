# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime
from typing import Optional

# Request Schema for Registration
class RegisterUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    password_confirmation: str
    role: int
    gender: Optional[int] = None 
    phone: Optional[str] = None  
    address: Optional[str] = None
    image: Optional[str] = None 

    @model_validator(mode='before')
    def check_password_match(cls, values):
        password = values.get('password')
        password_confirmation = values.get('password_confirmation')
        
        if password != password_confirmation:
            raise ValueError("Passwords do not match")
        
        return values
    
    class Config:
        from_attributes = True

# Response Schema for Registration
class RegisterUserResponse(BaseModel):
    message: str
    otp_code: int
    expires_in: int
    created_at: datetime
    role: str  # Role name instead of ID
    # gender: Optional[str]  # Gender name instead of ID (optional)

    class Config:
        from_attributes = True

# Request Schema for Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response Schema for Login
class TokenData(BaseModel):
    access_token: str
    access_expires_in: int
    refresh_token: str
    refresh_expires_in: int
    token_type: str = "Bearer"

class LoginResponse(BaseModel):
    message: str
    status: int
    type: str
    data: TokenData


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str  # Role name instead of ID
    gender: Optional[str] = None  # Gender name instead of ID (optional)
    phone: Optional[str] = None
    address: Optional[str] = None
    image: Optional[str] = None
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True
        orm_mode = True

class UserWrapper(BaseModel):
    user: UserResponse

# OTP Request Schema
class RequestOTPRequest(BaseModel):
    email: EmailStr  # User email for which OTP is requested

    class Config:
        from_attributes = True

class OTPResponseData(BaseModel):
    otp_code: str
    expires_in: int

class OTPResponse(BaseModel):
    message: str
    data: OTPResponseData  # Replace dict with a structured model

    class Config:
        from_attributes = True

# OTP Response Schema (message and OTP details)
class OTPResponse(BaseModel):
    message: str  # Response message
    data: dict  # Any additional data, like OTP code or expiry time

    class Config:
        from_attributes = True
        orm_mode = True

# OTP Verification Request Schema
class VerifyOTPRequest(BaseModel):
    email: str
    otp_code: str  # Ensure otp_code is defined here

    class Config:
        # The new FastAPI/Pydantic version uses `from_attributes` instead of `orm_mode`
        from_attributes = True

class OTPVerifyRequest(BaseModel):
    email: str
    otp_code: int

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str

class ChangeEmailRequest(BaseModel):
    current_email: EmailStr
    new_email: EmailStr

