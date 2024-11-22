# app\db\models\stripe.py
from sqlalchemy import Column, Integer, String, DateTime
from app.db.config import Base

from app.utility.utc import get_cambodia_time

class StripePayment(Base):
    __tablename__ = "stripe_payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_intent_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # Example: pending, succeeded, failed
    amount = Column(Integer)  # Store the payment amount in cents
    currency = Column(String, default="usd")
    created_at = Column(DateTime, default=get_cambodia_time) 

    @property
    def created_at_iso(self):
        return self.created_at.isoformat() if self.created_at else None