from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, EmailLog
from app.schemas.SMTP import OTPResponse
from app.utility.SMTP import send_otp_to_email
import pytz

# Cambodia timezone
CAMBODIA_TZ = pytz.timezone("Asia/Phnom_Penh")

def generate_and_send_otp(email: str, db: Session):
    # Check if user exists in the database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate OTP code using a cryptographically secure random generator
    otp_code = secrets.randbelow(1000000)  # Generate OTP in the range [0, 999999]

    # OTP expiration time (e.g., 10 minutes from now, Cambodia timezone)
    expiration_time = datetime.now(CAMBODIA_TZ) + timedelta(minutes=10)

    # Log the OTP in the database
    email_log = EmailLog(
        email=email,
        otp_code=otp_code,
        subject="Account Verification - OTP",
        body=f"Your OTP is: {otp_code}. It will expire in 10 minutes.",
        expiration_time=expiration_time,
        user_id=user.id  # Storing user ID for reference
    )
    db.add(email_log)
    db.commit()

    # Send OTP to the user's email and pass user_id
    send_otp_to_email(email, otp_code, user.id)

    # Return the response including the expiration time
    return OTPResponse(
        message=f"OTP sent successfully to {email}.",
        #otp_code=otp_code,  # For testing, you can remove this line in production
        expiration_time=expiration_time,
        timestamp=datetime.now(CAMBODIA_TZ)
    )
