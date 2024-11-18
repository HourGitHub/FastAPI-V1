# # app/api/SMTP/routes.py

from fastapi import APIRouter, Depends
from app.api.SMTP.controllers import generate_and_send_otp
from app.db import get_db
from app.schemas.SMTP import OTPRequest  # Assuming you have a schema for OTP requests
from sqlalchemy.orm import Session

SMTP = APIRouter()

@SMTP.post("/send_mail")
def send_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    # Now, otp_request contains the email passed in the body
    return generate_and_send_otp(otp_request.email, db)
