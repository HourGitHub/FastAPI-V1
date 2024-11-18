# app/api/auth/controllers.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import random
from app.db.models.utility import OTP, Gender, Role
from app.db.models.user import User

from app.schemas.auth import ChangeEmail, ForgotPasswordRequest, OtpRequest, OtpResponse, OtpVerify, RefreshTokenRequest, ResetPassword, UserCreate, UserLogin, UserResponse, UserUpdate
from app.security.auth import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.security.auth import verify_refresh_token

# User Registration Controller
def register_user(user_data, db: Session):
    # Fetch the Role and Gender objects from the database
    role = db.query(Role).filter(Role.id == user_data.role_id).first()
    gender = db.query(Gender).filter(Gender.id == user_data.gender_id).first()

    # If either role or gender is not found, raise an error
    if not role:
        raise ValueError(f"Role with ID {user_data.role_id} not found.")
    if not gender:
        raise ValueError(f"Gender with ID {user_data.gender_id} not found.")

    # Create the new user instance
    db_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password,
        role=role,  # Assign the Role instance
        gender=gender,  # Assign the Gender instance
        phone=user_data.phone,
        address=user_data.address,
        image=user_data.image,
    )
    
    # Add the user to the session and commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


# User Login Controller
def login_user(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Generate Tokens
    access_token = create_access_token(subject=db_user.email)
    refresh_token = create_refresh_token(subject=db_user.email)

    return {
        "message": "Login successful",
        "status": 200,
        "type": "jwt",
        "data": {
            "access_token": access_token,
            "access_expires_in": 3600,
            "refresh_token": refresh_token,
            "refresh_expires_in": 86400,
            "token_type": "Bearer"
        }
    }


# Request OTP Controller
def request_otp(otp_request: OtpRequest, db: Session):
    db_user = db.query(User).filter(User.email == otp_request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = random.randint(100000, 999999)  # Random 6-digit OTP
    otp = OTP(email=otp_request.email, otp_code=otp_code, expires_in=600, created_at=datetime.utcnow())
    db.add(otp)
    db.commit()

    return OtpResponse(message="OTP requested successfully.", data={
        "email": otp_request.email,
        "otp_code": otp_code,
        "expires_in": 600
    })


# Verify OTP Controller
def verify_otp(otp_data: OtpVerify, db: Session):
    otp = db.query(OTP).filter(OTP.email == otp_data.email, OTP.otp_code == otp_data.otp_code).first()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if otp.expires_in < datetime.utcnow().timestamp():
        raise HTTPException(status_code=400, detail="OTP has expired")

    return {"message": "OTP verified successfully. You can now log in.", "email": otp_data.email, "otp_code": otp_data.otp_code}


# Forgot Password Controller
def forgot_password(request: ForgotPasswordRequest, db: Session):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Logic to send password reset email here
    return {"message": "Password reset link sent to your email."}


# Reset Password Controller
def reset_password(reset_data: ResetPassword, db: Session):
    db_user = db.query(User).filter(User.reset_token == reset_data.reset_token).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid reset token")

    # Update password
    db_user.password = get_password_hash(reset_data.new_password)
    db.commit()
    return {"message": "Password reset successfully."}


# Change Email Controller
def change_email(email_data: ChangeEmail, db: Session):
    db_user = db.query(User).filter(User.email == email_data.current_email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.email = email_data.new_email
    db.commit()
    return {"message": "Email changed successfully."}


# Update User Info Controller
def update_user(user_id: int, user_data: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    return {"message": "User updated successfully."}


# Delete User Controller
def delete_user(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully."}


# Refresh Token Controller
def refresh_token(refresh_token: RefreshTokenRequest, db: Session):
    # Decode the refresh token, validate it, and then issue new tokens
    decoded_token = verify_refresh_token(refresh_token.refresh_token)  # Ensure you have a function to decode and validate the refresh token
    if not decoded_token:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    
    user_email = decoded_token['sub']  # Assuming 'sub' is the user email in the decoded token

    access_token = create_access_token(subject=user_email)
    refresh_token = create_refresh_token(subject=user_email)
    return {
        "message": "Tokens refreshed successfully.",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    }
