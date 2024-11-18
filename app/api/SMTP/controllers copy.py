from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, EmailLog
from app.schemas.SMTP import OTPResponse
from app.utility.SMTP import send_otp_to_email
from app.utility.utc import get_current_cambodia_time  

def generate_and_send_otp(email: str, db: Session):
    # Check if user exists in the database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate OTP code 
    otp_code = secrets.randbelow(1000000)  
    otp_code = str(otp_code).zfill(6)  

    # OTP expiration 
    expiration_time = get_current_cambodia_time() + timedelta(minutes=10)

    # Log the OTP in the database with timezone-aware expiration time
    email_log = EmailLog(
        email=email,
        otp_code=otp_code,
        subject="Account Verification - OTP",
        body=f"Your OTP is: {otp_code}. It will expire in 10 minutes.",
        expiration_time=expiration_time, 
        user_id=user.id 
    )
    db.add(email_log)
    db.commit()

    # Send OTP to the user's email and pass user_id
    send_otp_to_email(email, otp_code, user.id)

    # Return the response including the expiration time
    return OTPResponse(
        message=f"OTP sent successfully to {email}.",
        otp_code=otp_code,  
        expiration_time=expiration_time,
        timestamp=datetime.utcnow() 
    )
