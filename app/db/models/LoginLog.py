# app/db/models/login_log.py

from datetime import datetime
import pytz
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.db.config import Base
from sqlalchemy.orm import relationship

class LoginLog(Base):
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship
    user = relationship("User", back_populates="login_logs")

    def __repr__(self):
        return f"<LoginLog(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})>"
