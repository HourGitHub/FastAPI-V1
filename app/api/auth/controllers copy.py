# # app/api/auth/controllers.py

# from datetime import datetime, timedelta
# import random

# from jose import JWTError, jwt
# import pytz
# from app.db import models
# from fastapi import HTTPException, Response, status
# from sqlalchemy.orm import Session
# from app.db.models.utility import OTP, Gender, PasswordReset, Role
# from app.schemas.auth import  RegisterUserResponse, LoginRequest, LoginResponse, ResetPasswordRequest, TokenData, UserResponse
# from app.db.models import User
# from app.security.jwt import ALGORITHM, SECRET_KEY, create_access_token, create_refresh_token
# from app.security.passwords import get_password_hash, verify_user_password

# # Cambodia Timezone (GMT+7)
# CAMBODIA_TZ = pytz.timezone("Asia/Phnom_Penh")

# # Function to get the current logged-in user from the access token
# def get_current_user(db: Session, token: str):
#     try:
#         # Decode the JWT token using the 'jwt' module from 'jose'
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Token is invalid")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token is invalid")
    
#     # Fetch the user from the database
#     user = db.query(User).filter(User.email == email).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user

# # Function to convert user data into a response format
# def user_to_response(user: User) -> UserResponse:
#     role_name = user.role.name  # Get the role name (string)
#     gender_name = user.gender.name if user.gender else None  # Get the gender name (string)

#     return UserResponse(
#         id=user.id,
#         full_name=user.full_name,
#         email=user.email,
#         role=role_name,  # Pass the role name (string) instead of the ID
#         gender=gender_name,  # Pass the gender name (string) instead of the ID
#         phone=user.phone,
#         address=user.address,
#         image=user.image,
#         is_active=user.is_active,
#         created_at=user.created_at.isoformat(),  # Convert to string
#     )

# # Function to get all users
# def get_all_users(db: Session):
#     users = db.query(User).all()
#     if not users:
#         raise HTTPException(status_code=404, detail="No users found")

#     user_responses = []
#     for user in users:
#         role_name = user.role.name
#         gender_name = user.gender.name if user.gender else None

#         user_response = UserResponse(
#             id=user.id,
#             full_name=user.full_name,
#             email=user.email,
#             role=role_name,  # Use role name here
#             gender=gender_name,  # Use gender name here
#             phone=user.phone,
#             address=user.address,
#             image=user.image,
#             is_active=user.is_active,
#             created_at=user.created_at.isoformat(),  # Convert to string
#         )
#         user_responses.append(user_response)

#     return user_responses

# # Function to get a single user by ID
# def get_user(db: Session, user_id: int):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     role_name = user.role.name
#     gender_name = user.gender.name if user.gender else None

#     user_response = UserResponse(
#         id=user.id,
#         full_name=user.full_name,
#         email=user.email,
#         role=role_name,  # Use role name here
#         gender=gender_name,  # Use gender name here
#         phone=user.phone,
#         address=user.address,
#         image=user.image,
#         is_active=user.is_active,
#         created_at=user.created_at.isoformat(),  # Convert to string
#     )

#     return user_response

# def register_user(user_data, db: Session):
#     # Check if email already exists
#     existing_user = db.query(User).filter(User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Validate if passwords match
#     if user_data.password != user_data.password_confirmation:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Passwords do not match"
#         )

#     # Query for the Role and Gender by ID
#     role = db.query(Role).filter(Role.id == user_data.role).first()
#     gender = db.query(Gender).filter(Gender.id == user_data.gender).first() if user_data.gender else None

#     if not role:
#         raise HTTPException(status_code=404, detail="Role not found")
#     if user_data.gender and not gender:
#         raise HTTPException(status_code=404, detail="Gender not found")

#     # Hash the password before saving it
#     hashed_password = get_password_hash(user_data.password)

#     # Create the new User with is_active set to False initially
#     user = User(
#         full_name=user_data.full_name,
#         email=user_data.email,
#         hashed_password=hashed_password,  # Store the hashed password
#         role_id=user_data.role,
#         gender_id=user_data.gender,
#         phone=user_data.phone,
#         address=user_data.address,
#         image=user_data.image,
#         is_active=False  # User is not active yet
#     )

#     # Add the new user to the session
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # Generate OTP expiration time (1 hour from now)
#     expiry_time = datetime.utcnow() + timedelta(hours=1)

#     # Generate and send OTP (you already have this logic)
#     otp_code = random.randint(100000, 999999)  # OTP code
#     otp = OTP(email=user.email, otp_code=otp_code, expiration_time=expiry_time, user_id=user.id)
#     db.add(otp)
#     db.commit()

#     # Send OTP to user's email (this is where you'd send the actual OTP)
#     # send_otp_to_email(user.email, otp_code)  # You need to implement this function

#     return RegisterUserResponse(
#         message="User successfully registered. Please verify OTP to activate your account.",
#         otp_code=otp_code,
#         expires_in=3600,  # OTP expiry time (1 hour)
#         created_at=datetime.utcnow(),
#         role=role.name,
#         gender=gender.name if gender else None
#     )

# def login_user(login_data: LoginRequest, db: Session, response: Response):
#     # Fetch user by email
#     user = db.query(User).filter(User.email == login_data.email).first()

#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     # Check if user is active (verified)
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Account not yet verified. Please verify your OTP.")

#     # Verify password
#     if not verify_user_password(login_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid email or password")

#     # Generate access and refresh tokens
#     access_token = create_access_token(data={"sub": user.email})
#     refresh_token = create_refresh_token(data={"sub": user.email})

#     # Set the tokens in cookies
#     response.set_cookie(key="access_token", value=access_token, max_age=3600, httponly=True)
#     response.set_cookie(key="refresh_token", value=refresh_token, max_age=86400, httponly=True)

#     # Return the login response with tokens in body as well (optional)
#     return LoginResponse(
#         message="Login successful",
#         status=200,
#         type="jwt",
#         data=TokenData(
#             access_token=access_token,
#             access_expires_in=3600,  # 1 hour
#             refresh_token=refresh_token,
#             refresh_expires_in=86400,  # 1 day
#             token_type="Bearer"
#         )
#     )
# # Request OTP function (already in your code)
# def request_otp(email: str, db: Session):
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Check if an OTP already exists for the email
#     existing_otp = db.query(OTP).filter(OTP.email == email).first()
#     otp_code = random.randint(100000, 999999)
#     expires_in = 600  # OTP expires in 10 minutes
#     expiration_time = datetime.now(CAMBODIA_TZ) + timedelta(seconds=expires_in)

#     if existing_otp:
#         # Update existing OTP entry if it already exists
#         existing_otp.otp_code = otp_code
#         existing_otp.expiration_time = expiration_time
#         db.commit()
#     else:
#         # Create new OTP entry
#         otp = OTP(email=email, otp_code=otp_code, expiration_time=expiration_time, user_id=user.id)
#         db.add(otp)
#         db.commit()

#     # send_otp_to_email(email, otp_code)

#     return {
#         "message": "OTP requested successfully.",
#         "data": {
#             "email": email,
#             "otp_code": otp_code,  # Returning OTP for testing, remove in production
#             "expires_in": expires_in
#         }
#     }
# # Verify OTP function (already in your code)
# def verify_otp(db: Session, email: str, otp_code: str):
#     # Retrieve the OTP record for the user
#     otp_record = db.query(models.OTP).filter(models.OTP.email == email, models.OTP.otp_code == otp_code).first()
    
#     # Check if the OTP exists and is not expired
#     if otp_record:
#         # Make sure both datetimes are aware
#         if otp_record.expiration_time.tzinfo is None:
#             otp_record.expiration_time = CAMBODIA_TZ.localize(otp_record.expiration_time)
        
#         if otp_record.expiration_time < datetime.now(CAMBODIA_TZ):
#             return {"detail": "OTP has expired"}

#         # OTP is valid, proceed to update user status
#         user = db.query(models.User).filter(models.User.email == email).first()
        
#         if user:
#             user.is_active = True  # Update the user's status
#             db.commit()  # Commit the changes to the database
#             return {"message": "OTP verified successfully"}
#         else:
#             return {"detail": "User not found"}
#     else:
#         return {"detail": "Invalid OTP"}

# # Forgot Password function
# def forgot_password(email: str, db: Session):
#     user = db.query(User).filter_by(email=email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     reset_token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)
    
#     password_reset = PasswordReset(user_id=user.id, token=reset_token)
#     db.add(password_reset)
#     db.commit()

#     # send_password_reset_email(user.email, reset_token)  # Implement this function

#     return {
#         "message": "Password reset link sent to your email.",
#         "reset_token": reset_token  # Returning for testing purposes
#     }

# # Reset Password function
# def reset_password(data: ResetPasswordRequest, db: Session):
#     try:
#         payload = jwt.decode(data.reset_token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=400, detail="Invalid reset token")

#         user = db.query(User).filter_by(email=email).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         # Hash the new password
#         new_password_hashed = get_password_hash(data.new_password)
#         user.hashed_password = new_password_hashed
#         db.commit()

#         return {"message": "Password reset successfully."}
#     except JWTError:
#         raise HTTPException(status_code=400, detail="Invalid reset token")

# # Change Email function
# def change_email(current_email: str, new_email: str, db: Session):
#     user = db.query(User).filter_by(email=current_email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     user_with_new_email = db.query(User).filter_by(email=new_email).first()
#     if user_with_new_email:
#         raise HTTPException(status_code=400, detail="New email is already in use")

#     user.email = new_email
#     db.commit()

#     return {"message": "Email changed successfully."}

