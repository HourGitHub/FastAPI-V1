# app/api/auth/routes.py

from typing import Dict
from app.security.jwt import get_access_token
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.api.auth.controllers import change_email, forgot_password, get_all_users, get_current_user, get_user, register_user, login_user, request_otp, reset_password, user_to_response, verify_otp
from app.db.config import get_db
from app.schemas.auth import ChangeEmailRequest, ForgotPasswordRequest, LoginResponse, OTPVerifyRequest, RegisterUserRequest, LoginRequest, RegisterUserResponse, RequestOTPRequest, ResetPasswordRequest, UserResponse, UserWrapper


auth = APIRouter()

# Route to get the current logged-in user
@auth.get("/current-user", response_model=UserResponse)
def get_current_user_route(db: Session = Depends(get_db), token: str = Depends(get_access_token)):
    # Get the current user by passing the token and the DB session
    user = get_current_user(db=db, token=token)
    
    # Convert the user to a response format
    return user_to_response(user)

# Route for fetching all users
@auth.get("/users", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db)):
    return get_all_users(db=db)

# Route for fetching a user by ID

@auth.get("/users/{user_id}", response_model=Dict[str, UserResponse])
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


# Route for fetching a user by ID
@auth.get("/users/{user_id}", response_model=UserWrapper)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    # Retrieve the user using your function
    user_response = get_user(db=db, user_id=user_id)
    # Return the response wrapped in the 'user' key
    return {"user": user_response}

@auth.post("/register", response_model=RegisterUserResponse)
def register_user_route(user_data: RegisterUserRequest, db: Session = Depends(get_db)):
    try:
        return register_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return login_user(login_data=request, db=db, response=response)

# Request OTP route
@auth.post("/request-otp")
def request_otp_endpoint(data: RequestOTPRequest, db: Session = Depends(get_db)):
    return request_otp(data.email, db)

# Verify OTP route
@auth.post("/verify-otp")
def verify_otp_route(otp_request: OTPVerifyRequest, db: Session = Depends(get_db)):
    return verify_otp(email=otp_request.email, otp_code=otp_request.otp_code, db=db)

# Forgot Password route
@auth.post("/forgot-password")
def forgot_password_endpoint(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(data.email, db)

# Reset Password route
@auth.post("/reset-password")
def reset_password_endpoint(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(data, db)

# Change Email route
@auth.post("/change-email")
def change_email_endpoint(data: ChangeEmailRequest, db: Session = Depends(get_db)):
    return change_email(data.current_email, data.new_email, db)