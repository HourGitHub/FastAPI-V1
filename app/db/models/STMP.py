# app/db/models/STMP.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.config import Base
from app.db.models import User
import pytz

CAMBODIA_TZ = pytz.timezone('Asia/Phnom_Penh')

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)  # The email recipient
    otp_code = Column(Integer)  # OTP code sent
    subject = Column(String)  # Subject of the email
    body = Column(String)  # Body content of the email
    sent_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the email was sent
    is_verified = Column(Boolean, default=False)  # Verification status (true/false)
    expiration_time = Column(DateTime, default=lambda: datetime.now(CAMBODIA_TZ), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Link to the user
    user = relationship("User", back_populates="email_logs")

    def __repr__(self):
        return f"<EmailLog(id={self.id}, email={self.email}, otp_code={self.otp_code}, sent_at={self.sent_at})>"
