# app/db/models/utility.py

from datetime import datetime, timedelta
import pytz
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.config import Base

# Brand
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # products = relationship("Product", back_populates="brand")


# Category
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # stocks = relationship("StockItem", back_populates="category")
    # products = relationship("Product", back_populates="category")


# Color
class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # products = relationship("Product", back_populates="color")


# Gender
class Gender(Base):
    __tablename__ = 'genders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    users = relationship("User", back_populates="gender", passive_deletes=True)

    def __repr__(self):
        return f"<Gender(id={self.id}, name='{self.name}', created_at={self.created_at})>"


# Model
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # products = relationship("Product", back_populates="model")


# Role
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    users = relationship("User", back_populates="role", passive_deletes=True)


# Supplier
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    location = Column(String, nullable=True)  # Ensure location is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
    status = Column(String, default="active")

    # stocks = relationship("StockItem", back_populates="supplier")


# Unit
class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    abbreviation = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # stocks = relationship("StockItem", back_populates="unit")


# StockStatus
class StockStatus(Base):
    __tablename__ = "stock_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)  # Ensure description is nullable if optional
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))

    # products = relationship("Product", back_populates="stock_status")
    # stock_items = relationship("StockItem", back_populates="stock_status")

    def __repr__(self):
        return f"<StockStatus(id={self.id}, name='{self.name}')>"


# Otp
class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp_code = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
    expiry_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))

    def is_expired(self):
        return datetime.utcnow() > self.expiry_at


# Password Reset
class PasswordReset(Base):
    __tablename__ = "password_resets"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    token = Column(String, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
    expiry_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))

    def is_expired(self):
        return datetime.utcnow() > self.expiry_at


# # Token Blacklist
# class TokenBlacklist(Base):
#     __tablename__ = "token_blacklist"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     refresh_token = Column(String)
#     created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Bangkok')))
#     user = relationship("User")

