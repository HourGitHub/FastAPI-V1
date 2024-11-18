# app/schemas/utility.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# =====================
# Brand
# =====================
class BrandCreate(BaseModel):
    name: str
    description: str

class BrandResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Category
# =====================
class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Color
# =====================
class ColorCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ColorResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Gender
# =====================
class GenderCreate(BaseModel):
    name: str
    description: Optional[str] = None

class GenderResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Model
# =====================
class ModelCreate(BaseModel):
    name: str
    description: str

class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Role
# =====================
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Status
# =====================
class StockStatusCreate(BaseModel):
    name: str
    description: str

# StockStatusResponse schema for returning stock status details in response
class StockStatusResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime  # Ensure the field is returned as a datetime object

    class Config:
        from_attributes = True
        orm_mode = True


# =====================
# Supplier
# =====================
class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class SupplierCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = "active"

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: ContactInfo
    status: str

    class Config:
        from_attributes = True
        orm_mode = True

    @classmethod
    def from_orm(cls, supplier):
        return cls(
            id=supplier.id,
            name=supplier.name,
            contact_info=ContactInfo(
                email=supplier.email,
                phone=supplier.phone,
                location=supplier.location,
            ),
            status=supplier.status,
        )


# =====================
# Unit
# =====================
class UnitCreate(BaseModel):
    name: str
    abbreviation: str
    description: str

class UnitResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
    created_at: datetime
    description: str

    class Config:
        from_attributes = True
        orm_mode = True
