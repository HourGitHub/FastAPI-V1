# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# User Create Schema
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: int  # 1 = Admin, 2 = User
    gender: int  # 1 = Male, 2 = Female
    phone: Optional[str] = None
    address: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True


# User Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# User Response Schema (used for registration success and OTP response)
class UserResponse(BaseModel):
    message: str
    otp_code: int
    expires_in: int  # in seconds
    created_at: datetime
    role: str  # "Admin" or "User"

    class Config:
        from_attributes = True


# OTP Request Schema (used when requesting an OTP)
class OtpRequest(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


# OTP Response Schema (used to return OTP details)
class OtpResponse(BaseModel):
    message: str
    data: dict

    class Config:
        from_attributes = True


# OTP Verify Schema (used when verifying OTP)
class OtpVerify(BaseModel):
    email: EmailStr
    otp_code: int

    class Config:
        from_attributes = True


# Forgot Password Request Schema (used to request a password reset link)
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


# Reset Password Schema (used to reset the password)
class ResetPassword(BaseModel):
    reset_token: str
    new_password: str

    class Config:
        from_attributes = True


# Change Email Schema (used for changing the user's email)
class ChangeEmail(BaseModel):
    current_email: EmailStr
    new_email: EmailStr

    class Config:
        from_attributes = True


# User Update Schema (used for updating user information)
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[int] = None  # Assuming 1 = Admin, 2 = User
    gender: Optional[int] = None  # 1 = Male, 2 = Female
    phone: Optional[str] = None
    address: Optional[str] = None
    image: Optional[str] = None

    # Custom validators for role and gender to ensure they are within valid range
    @validator('role')
    def validate_role(cls, value):
        if value is not None and value not in [1, 2]:
            raise ValueError('Role must be 1 (Admin) or 2 (User)')
        return value

    @validator('gender')
    def validate_gender(cls, value):
        if value is not None and value not in [1, 2]:
            raise ValueError('Gender must be 1 (Male) or 2 (Female)')
        return value

    class Config:
        from_attributes = True


# Refresh Token Request Schema (used for refreshing access tokens)
class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str  # e.g., "bearer"
    expires_in: int  # in seconds

    class Config:
        from_attributes = True