from datetime import datetime, timedelta
import random

from jose import JWTError, jwt
import pytz
from app.db import models
from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.models.utility import OTP, Gender, PasswordReset, Role
from app.schemas.auth import RegisterUserResponse, LoginRequest, LoginResponse, ResetPasswordRequest, TokenData, UserResponse
from app.db.models import User
from app.security.jwt import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token
from app.security.passwords import get_password_hash, verify_user_password
from app.utility.SMTP import send_otp_to_email

# Cambodia Timezone (GMT+7)
CAMBODIA_TZ = pytz.timezone("Asia/Phnom_Penh")

# Function to get the current logged-in user from the access token
def get_current_user(db: Session, token: str):
    try:
        # Decode the JWT token using the 'jwt' module from 'jose'
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    
    # Fetch the user from the database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Function to convert user data into a response format
def user_to_response(user: User) -> UserResponse:
    role_name = user.role.name  # Get the role name (string)
    gender_name = user.gender.name if user.gender else None  # Get the gender name (string)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=role_name,  # Pass the role name (string) instead of the ID
        gender=gender_name,  # Pass the gender name (string) instead of the ID
        phone=user.phone,
        address=user.address,
        image=user.image,
        is_active=user.is_active,
        created_at=user.created_at.astimezone(CAMBODIA_TZ).isoformat(),  # Convert to Cambodia timezone and string
    )

# Function to get all users
def get_all_users(db: Session):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    user_responses = []
    for user in users:
        role_name = user.role.name
        gender_name = user.gender.name if user.gender else None

        user_response = UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=role_name,  # Use role name here
            gender=gender_name,  # Use gender name here
            phone=user.phone,
            address=user.address,
            image=user.image,
            is_active=user.is_active,
            created_at=user.created_at.astimezone(CAMBODIA_TZ).isoformat(),  # Convert to Cambodia timezone and string
        )
        user_responses.append(user_response)

    return user_responses

def login_user(login_data: LoginRequest, db: Session, response: Response):
    # Fetch user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Check if user is active (verified)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account not yet verified. Please verify your OTP.")

    # Verify password
    if not verify_user_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate access and refresh tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    # Set the tokens in cookies
    response.set_cookie(key="access_token", value=access_token, max_age=3600, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=86400, httponly=True)

    # Return the login response with tokens in body as well (optional)
    return LoginResponse(
        message="Login successful",
        status=200,
        type="jwt",
        data=TokenData(
            access_token=access_token,
            access_expires_in=3600,  # 1 hour
            refresh_token=refresh_token,
            refresh_expires_in=86400,  # 1 day
            token_type="Bearer"
        )
    )

# Function to get a single user by ID
def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_name = user.role.name
    gender_name = user.gender.name if user.gender else None

    user_response = UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=role_name,  # Use role name here
        gender=gender_name,  # Use gender name here
        phone=user.phone,
        address=user.address,
        image=user.image,
        is_active=user.is_active,
        created_at=user.created_at.astimezone(CAMBODIA_TZ).isoformat(),  # Convert to Cambodia timezone and string
    )

    return user_response

# Function to register a new user
def register_user(user_data, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate if passwords match
    if user_data.password != user_data.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Query for the Role and Gender by ID
    role = db.query(Role).filter(Role.id == user_data.role).first()
    gender = db.query(Gender).filter(Gender.id == user_data.gender).first() if user_data.gender else None

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if user_data.gender and not gender:
        raise HTTPException(status_code=404, detail="Gender not found")

    # Hash the password before saving it
    hashed_password = get_password_hash(user_data.password)

    # Create the new User with is_active set to False initially
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,  # Store the hashed password
        role_id=user_data.role,
        gender_id=user_data.gender,
        phone=user_data.phone,
        address=user_data.address,
        image=user_data.image,
        is_active=False  # User is not active yet
    )

    # Add the new user to the session
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate OTP expiration time (5 minutes from now)
    expiry_time = datetime.now(CAMBODIA_TZ) + timedelta(minutes=5)

    # Generate OTP (6-digit OTP code)
    otp_code = random.randint(100000, 999999)
    otp = OTP(email=user.email, otp_code=otp_code, expiration_time=expiry_time, user_id=user.id)
    db.add(otp)
    db.commit()

    # Try sending OTP to user's email (wrap in try-except for better error handling)
    try:
        send_otp_to_email(user.email, otp_code, user.id)  # Pass user.id here
    except Exception as e:
        db.rollback()  # Rollback the transaction if OTP sending fails
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")

    # Return response confirming user registration
    return RegisterUserResponse(
        message="User successfully registered. Please verify OTP to activate your account.",
        otp_code=otp_code,  # Include the OTP code in the response (remove in production)
        expires_in=300,  # OTP expiry time (5 minutes)
        created_at=datetime.now(CAMBODIA_TZ),
        role=role.name,
        gender=gender.name if gender else None
    )



# Verify OTP function (already in your code)
def verify_otp(db: Session, email: str, otp_code: str):
    # Retrieve the OTP record for the user
    otp_record = db.query(models.OTP).filter(models.OTP.email == email, models.OTP.otp_code == otp_code).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Ensure expiration_time is aware (localized to CAMBODIA_TZ)
    if otp_record.expiration_time.tzinfo is None:
        otp_record.expiration_time = CAMBODIA_TZ.localize(otp_record.expiration_time)


    # Compare with the current time in the same timezone
    if otp_record.expiration_time < datetime.now(CAMBODIA_TZ):
        raise HTTPException(status_code=400, detail="OTP has expired")


    # OTP is valid, proceed to activate the user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True  # Update the user's status to active
    db.commit()  # Commit the changes to the database

    return {"message": "OTP verified successfully. You can now log in."}


# Request OTP function
def request_otp(email: str, db: Session):
    # Retrieve the user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the account is already active
    if user.is_active:
        raise HTTPException(status_code=400, detail="Account is already active")

    # Generate a new OTP
    otp_code = random.randint(100000, 999999)
    expiry_time = datetime.now(CAMBODIA_TZ) + timedelta(minutes=5)

    # Update or create an OTP entry in the database
    existing_otp = db.query(OTP).filter(OTP.email == email).first()
    if existing_otp:
        existing_otp.otp_code = otp_code
        existing_otp.expiration_time = expiry_time
    else:
        new_otp = OTP(email=email, otp_code=otp_code, expiration_time=expiry_time, user_id=user.id)
        db.add(new_otp)

    db.commit()

    # Send the OTP to the user's email
    try:
        send_otp_to_email(email, otp_code, user.id)
    except Exception as e:
        db.rollback()  # Rollback in case of failure to send the OTP
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {str(e)}")

    return {"message": "OTP has been sent to your email.", "otp_code": otp_code, "expires_in": 300}



# Forgot Password function
def forgot_password(email: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account not verified. Please verify OTP before resetting password.")

    # Generate reset token and expiry
    reset_token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)

    expiry_time = datetime.now(CAMBODIA_TZ) + timedelta(minutes=10)
    password_reset = PasswordReset(
        user_id=user.id,
        email=user.email,
        token=reset_token,
        expiry_at=expiry_time
    )

    db.add(password_reset)
    db.commit()

    send_otp_to_email(user.email, reset_token, user.id)  # Implement the email function

    return {
        "message": "Password reset link sent to your email.",
        "reset_token": reset_token  # Returning for testing purposes
    }

# Reset Password function
def reset_password(data: ResetPasswordRequest, db: Session):
    try:
        # Decode and validate the reset token
        payload = jwt.decode(data.reset_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid reset token")

        # Check if a valid PasswordReset entry exists for this token
        reset_entry = db.query(PasswordReset).filter_by(token=data.reset_token).first()
        if not reset_entry:
            raise HTTPException(status_code=400, detail="Reset token not found or already used.")

        # Ensure token hasn't expired
        if reset_entry.expiry_time < datetime.now(CAMBODIA_TZ):
            raise HTTPException(status_code=400, detail="Reset token has expired")

        # Get the user associated with the reset request
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Hash the new password and update the user's password
        new_password_hashed = get_password_hash(data.new_password)
        user.hashed_password = new_password_hashed
        db.commit()

        # Clean up the used reset token
        db.delete(reset_entry)
        db.commit()

        return {"message": "Password reset successfully."}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid reset token")

# Change Email function
def change_email(current_email: str, new_email: str, db: Session):
    user = db.query(User).filter_by(email=current_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_with_new_email = db.query(User).filter_by(email=new_email).first()
    if user_with_new_email:
        raise HTTPException(status_code=400, detail="New email is already in use")

    user.email = new_email
    db.commit()

    return {"message": "Email changed successfully."}

