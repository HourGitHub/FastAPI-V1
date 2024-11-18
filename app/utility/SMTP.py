import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from app.db import SessionLocal
from app.db.models.STMP import EmailLog
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

def send_otp_to_email(to_email: str, otp_code: int, user_id: int):
    """
    Send OTP email to the user and log the email in the database.
    """
    # Get email settings from environment variables
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    # Check if the environment variables are loaded properly
    if not sender_email or not sender_password:
        print("Error: Email address or password is not set in .env file.")
        return

    subject = "Account Verification - OTP"
    body = f"Your OTP for account verification is: {otp_code}. It will expire in 1 hour."

    # Create MIME message for the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # SSL connection
        print(f"Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        print(f"Sending email to {to_email}...")
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()  # Close the server connection
        print("OTP sent successfully!")

        # Log the email in the database
        expiration_time = datetime.utcnow() + timedelta(hours=1)  # OTP expiration time
        with SessionLocal() as db:  # Use context manager for automatic closing
            email_log = EmailLog(
                email=to_email,
                otp_code=otp_code,
                subject=subject,
                body=body,
                sent_at=datetime.utcnow(),
                expiration_time=expiration_time,
                user_id=user_id
            )
            db.add(email_log)
            db.commit()  # Commit the log to the database
            print(f"OTP for {to_email} logged successfully in the database.")

    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        # You can also log the exception to a file or monitoring service if needed

