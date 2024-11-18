# app/db/models/STMP.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.config import Base
from app.db.models import User

from app.utility.utc import get_current_cambodia_time

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)  # The email recipient
    otp_code = Column(Integer)  # OTP code sent
    subject = Column(String)  # Subject of the email
    body = Column(String)  # Body content of the email
    sent_at = Column(DateTime, default=get_current_cambodia_time) 
    is_verified = Column(Boolean, default=False)  # Verification status (true/false)
    expiration_time = Column(DateTime, default=get_current_cambodia_time) 
    user_id = Column(Integer, ForeignKey("users.id"))  # Link to the user
    user = relationship("User", back_populates="email_logs")

    def __repr__(self):
        return f"<EmailLog(id={self.id}, email={self.email}, otp_code={self.otp_code}, sent_at={self.sent_at})>"
