# app/db/models/login_log.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.config import Base
from datetime import datetime

from app.utility.utc import get_current_cambodia_time

class LoginLog(Base):
    __tablename__ = 'login_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action_type = Column(String, nullable=False) 
    timestamp = Column(DateTime, default=get_current_cambodia_time) 
    ip_address = Column(String, nullable=True) 
    success = Column(Boolean, default=True)  
    user_agent = Column(String, nullable=True) 
    additional_info = Column(String, nullable=True)

    # Relationship to User model 
    user = relationship("User", back_populates="login_logs")

    def __repr__(self):
        return f"<LoginLog(id={self.id}, user_id={self.user_id}, action_type='{self.action_type}', success={self.success}, timestamp={self.timestamp})>"

