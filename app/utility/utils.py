# app/utility/utils.py

import random
import string
# If you're using email sending functionality, keep FastMail imports
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Generate OTP
def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

# Send OTP (this is just a placeholder, configure your email service accordingly)
def send_otp(email: str, otp: str):
    # Here you would integrate with your email service (e.g., SMTP)
    pass

