# app/schemas/SMTP.py

from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta


class EmailSchema(BaseModel):
    email: List[EmailStr]
    
# Schema for OTP Request (User providing email)
class OTPRequest(BaseModel):
    email: EmailStr  # The email to which OTP will be sent

# Schema for OTP Response (API response after sending OTP)
class OTPResponse(BaseModel):
    message: str
    otp_code: int  # For testing, you can remove this in production
    expiration_time: datetime  # When the OTP expires
    timestamp: datetime

    class Config:
        # Allow returning datetime as string (ISO format)
        orm_mode = True

    # Optional: You can exclude otp_code in production by adding a method
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if "otp_code" in data:
            del data["otp_code"]  # Remove OTP code in production
        return data
