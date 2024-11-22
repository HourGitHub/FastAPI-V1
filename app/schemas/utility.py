# app/schemas/utility.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.db.models.utility import Supplier

# =====================
# Status
# =====================

class StockStatusCreate(BaseModel):
    name: str  # Now just a plain string for name
    description: Optional[str] = None  # Optional description

# StatusResponse schema, keeping name as string
class StatusResponse(BaseModel):
    id: int
    name: str  # Keep it as a plain string for name
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True




class RoleCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None  # Optional description for the role

    class Config:
        from_attributes = True

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

class GenderCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None  # Optional description for gender

    class Config:
        from_attributes = True

class GenderResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

# =====================
# Brand
# =====================
class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None  # Optional description

class BrandResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

# =====================
# Category
# =====================
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None  # Optional description

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

# =====================
# Color
# =====================
class ColorCreate(BaseModel):
    name: str
    description: Optional[str] = None  # Optional field

class ColorResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

# =====================
# Models
# =====================
class ModelCreate(BaseModel):
    name: str
    description: Optional[str] = None  # Optional description

class ModelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # Optional description
    created_at: datetime  # Added created_at

    class Config:
        from_attributes = True

# =====================
# Supplier
# =====================
class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class SupplierCreate(BaseModel):
    name: str
    contact_info: Optional[ContactInfo] = None  # The contact_info field now holds email, phone, and location
    status: Optional[str] = "active"  # Default is 'active'

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: ContactInfo  # ContactInfo is part of the response
    status: str
    created_at: datetime  # Automatically generated on supplier creation

    class Config:
        from_attributes = True



# =====================
# Units
# =====================
class UnitCreate(BaseModel):
    name: str
    abbreviation: str
    description: Optional[str] = None  # Optional description

class UnitResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    created_at: datetime  # Added created_at
    description: Optional[str] = None  # Optional description

    class Config:
        from_attributes = True


# =====================
# Stripe
# =====================



# Request model for creating payment intent
class PaymentRequest(BaseModel):
    amount: int  
    currency: Optional [str] = "usd"  
    payment_method: str  
    expiry_date: Optional[str] = None  
    cvc: Optional [str] = None  
    name_on_card: Optional[str] = None  

    class Config:
        orm_mode = True

# Request model for confirming payment
class PaymentConfirmation(BaseModel):
    payment_intent_id: str  # ID of the payment intent to confirm

# Response model for payment status
class PaymentStatusResponse(BaseModel):
    status: str  # Status of the payment

class PaymentListItem(BaseModel):
    payment_intent_id: str  # Payment intent ID
    status: str  # Status of the payment (e.g., "succeeded", "pending", "failed")
    amount: int  # Amount in cents (e.g., 1000 for $10.00)
    currency: str  # The currency used for the payment
    created_at: str  # The timestamp when the payment was created (ISO 8601 format)

    class Config:
        orm_mode = True 