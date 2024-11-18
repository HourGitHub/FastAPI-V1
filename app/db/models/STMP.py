# app/db/models/STMP.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.config import Base
import pytz

# Cambodia timezone
CAMBODIA_TZ = pytz.timezone("Asia/Phnom_Penh")

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp_code = Column(Integer)
    subject = Column(String)
    body = Column(String)
    sent_at = Column(DateTime, default=lambda: datetime.now(CAMBODIA_TZ))
    is_verified = Column(Boolean, default=False)
    expiration_time = Column(DateTime, default=lambda: datetime.now(CAMBODIA_TZ) + timedelta(minutes=10), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="email_logs")

    def __repr__(self):
        return f"<EmailLog(id={self.id}, email={self.email}, otp_code={self.otp_code}, sent_at={self.sent_at})>"

