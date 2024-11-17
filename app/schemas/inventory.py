# app/schemas/inventory.py

from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


# ====================
# === REQUEST SCHEMAS ===
# ====================

class Product(BaseModel):
    itemId: str
    itemName: str
    categoryId: int
    unitId: int
    quantityAdded: int
    quantityInStock: int
    purchaseDate: date
    purchasePrice: float
    expiryDate: Optional[date]
    barcode: Optional[str]
    remark: Optional[str]
    restockLevel: Optional[int]
    supplierId: Optional [int]
    statusId: Optional [int]  # Correctly define statusId as per the request payload
    image: Optional[str]

    class Config:
        from_attributes = True


class StockItemUpdate(BaseModel):
    item_name: Optional[str]
    category_id: Optional[int]
    unit_id: Optional[int]
    quantity_added: Optional[int]
    quantity_in_stock: Optional[int]
    purchase_date: Optional[datetime]
    purchase_price: Optional[float]
    expiry_date: Optional[date]
    barcode: Optional[str]
    remark: Optional[str]
    restock_level: Optional[int]
    supplier_id: Optional[int]
    stock_status_id: Optional[int]
    image: Optional[str]
    
    class Config:
        from_attributes = True


# ====================
# === RESPONSE SCHEMAS ===
# ====================

class StockItemResponse(BaseModel):
    id: int
    item_id: str
    item_name: str
    category_name: Optional[str] = None
    unit_name: Optional[str] = None
    quantity_added: int
    quantity_in_stock: int
    purchase_date: date
    purchase_price: float
    expiry_date: Optional[date] = None
    barcode: Optional [str] = None
    remark: Optional[str] = None
    restock_level: int
    supplier_name: Optional[str] = None
    status: Optional[str] = None
    timestamp: datetime
    image: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True


# ====================
# === STOCK STATUS SCHEMAS ===
# ====================

class StockStatusCreate(BaseModel):
    name: str
    description: Optional[str] = None


class StatusResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ====================
# === ERROR RESPONSE ===
# ====================

class ErrorResponse(BaseModel):
    message: str
    status: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
