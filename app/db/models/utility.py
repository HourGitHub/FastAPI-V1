# app/db/models/utility.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.config import Base
from datetime import datetime
from sqlalchemy.orm import relationship

from app.utility.utc import CAMBODIA_TZ, get_current_cambodia_time


# Brand
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    products = relationship("Product", back_populates="brand")


# Category
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    stocks = relationship("StockItem", back_populates="category")
    products = relationship("Product", back_populates="category")


# Color
class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    products = relationship("Product", back_populates="color")


# Gender
class Gender(Base):
    __tablename__ = 'genders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    users = relationship("User", back_populates="gender")

    def __repr__(self):
        return f"<Gender(id={self.id}, name='{self.name}', created_at={self.created_at})>"


# Model
class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    products = relationship("Product", back_populates="model")


# Role
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"


# Supplier
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, nullable=True, default="active")
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    # Relationship example (if needed)
    stocks = relationship("StockItem", back_populates="supplier")


# Unit
class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    abbreviation = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    stocks = relationship("StockItem", back_populates="unit")


# StockStatus
class StockStatus(Base):
    __tablename__ = "stock_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_cambodia_time) 

    # Relationship to Product and StockItem
    products = relationship("Product", back_populates="stock_status")
    stock_items = relationship("StockItem", back_populates="stock_status")


# OTP Model
class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # Ensure it's unique for each user.
    otp_code = Column(Integer)
    expiration_time = Column(DateTime, default=get_current_cambodia_time) 
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="otp_codes")

    def __repr__(self):
        return f"<OTP(email={self.email}, otp_code={self.otp_code}, expiration_time={self.expiration_time})>"


# Password Reset
class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    token = Column(String, index=True)
    expiry_at = Column(DateTime, default=get_current_cambodia_time) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def is_expired(self):
        return datetime.now(CAMBODIA_TZ) > self.expiration_time

