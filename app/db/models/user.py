# app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.db.config import Base

# Avoid circular imports by using string reference for LoginLog
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    gender_id = Column(Integer, ForeignKey("genders.id"))
    phone = Column(String(15), nullable=True)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
    is_active = Column(Boolean, default=False)

    # Relationships
    role = relationship("Role", back_populates="users", single_parent=True)  # Ensure Role has `users` back_populates
    gender = relationship("Gender", back_populates="users")  # Ensure Gender has `users` back_populates
    login_logs = relationship("LoginLog", back_populates="user")  # Reference LoginLog as a string

    def __repr__(self):
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}', is_active={self.is_active})>"
