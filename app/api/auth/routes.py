# app/api/auth/routes.py

from fastapi import APIRouter, Depends
from app.api.auth.controllers import (
    register_user, login_user, request_otp, verify_otp, forgot_password, reset_password, 
    change_email, update_user, delete_user
)

from sqlalchemy.orm import Session 
from app.db import get_db
from app.schemas.auth import ChangeEmail, ForgotPasswordRequest, OtpRequest, OtpResponse, OtpVerify, RefreshTokenRequest, RefreshTokenResponse, ResetPassword, UserCreate, UserLogin, UserResponse, UserUpdate

auth_router = APIRouter()

# User Registration Endpoint
@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


# User Login Endpoint
@auth_router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)


# Request OTP Endpoint
@auth_router.post("/request-otp", response_model=OtpResponse)
def request_otp(otp_request: OtpRequest, db: Session = Depends(get_db)):
    return request_otp(otp_request, db)


# Verify OTP Endpoint
@auth_router.post("/verify-otp")
def verify_otp(otp_data: OtpVerify, db: Session = Depends(get_db)):
    return verify_otp(otp_data, db)


# Forgot Password Endpoint
@auth_router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(request, db)


# Reset Password Endpoint
@auth_router.post("/reset-password")
def reset_password(reset_data: ResetPassword, db: Session = Depends(get_db)):
    return reset_password(reset_data, db)


# Change Email Endpoint
@auth_router.put("/change-email")
def change_email(email_data: ChangeEmail, db: Session = Depends(get_db)):
    return change_email(email_data, db)


# Update User Info Endpoint
@auth_router.put("/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, user_data, db)


# Delete User Endpoint
@auth_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)


# Refresh Token Endpoint
@auth_router.post("/refresh-token", response_model=RefreshTokenResponse)
def refresh(refresh_token: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_token(refresh_token, db)
