# app/db/models/login_log.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.config import Base
from datetime import datetime
import pytz

# Define Cambodia Timezone
CAMBODIA_TZ = pytz.timezone('Asia/Phnom_Penh')

class LoginLog(Base):
    __tablename__ = 'login_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action_type = Column(String, nullable=False)  # e.g., 'login', 'logout', 'failed_login'
    timestamp = Column(DateTime, default=lambda: datetime.now(CAMBODIA_TZ))  # When the action happened
    ip_address = Column(String, nullable=True)  # IP address of the user
    success = Column(Boolean, default=True)  # Whether the action was successful or not
    user_agent = Column(String, nullable=True)  # Information about the device or browser
    additional_info = Column(String, nullable=True)  # Additional info like error message, etc.

    # Relationship to User model (assuming the user model exists)
    user = relationship("User", back_populates="login_logs")

    def __repr__(self):
        return f"<LoginLog(id={self.id}, user_id={self.user_id}, action_type='{self.action_type}', success={self.success}, timestamp={self.timestamp})>"

