# app/db/models/user.py

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from app.db.config import Base
from datetime import datetime
import pytz
from sqlalchemy.orm import relationship
from app.db.models.login_log import LoginLog

# Define the Cambodia time zone
CAMBODIA_TZ = pytz.timezone('Asia/Phnom_Penh')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True) 
    phone = Column(String, nullable=True)  
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=False) 

    # Use DateTime for created_at with timezone support
    created_at = Column(DateTime, default=lambda: datetime.now(CAMBODIA_TZ), nullable=False)

    # Relationships
    role = relationship("Role", back_populates="users")
    gender = relationship("Gender", back_populates="users")
    otp_codes = relationship("OTP", back_populates="user")
    login_logs = relationship("LoginLog", back_populates="user") 
    email_logs = relationship("EmailLog", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
