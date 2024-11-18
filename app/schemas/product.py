# app/schemas/product.py
from pydantic import BaseModel, root_validator
from typing import Optional, List
from datetime import date, datetime

class StockItemResponse(BaseModel):
    itemId: str
    itemName: str
    quantityInStock: int
    expiryDate: Optional[date] 
    unitName: Optional[str]    
    categoryName: Optional[str] 
    status: Optional[str]     
    barcode: Optional[str]     

    class Config:
        orm_mode = True
        # This ensures that datetime objects are converted to strings automatically.
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None  # Convert datetime to ISO format string
        }


class ProductCreate(BaseModel):
    productcode: str
    title: str
    price: float
    description: str
    brand_id: int
    model_id: int
    color_id: int
    category_id: int
    discount: Optional[float] = 0.0
    rating: Optional[float] = 0.0
    warranty: str
    status_id: int
    image: str
    stockItemId: str

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    id: int
    productcode: str
    title: str
    price: float
    description: Optional[str] = None
    brand_name: Optional[str] = None  
    model_name: Optional[str] = None  
    color_name: Optional[str] = None  
    category_name: str 
    discount: Optional[float] = None
    rating: Optional[float] = None
    warranty: Optional[str] = None
    stock_status_name: Optional[str] = None 
    image: Optional[str] = None
    created_at: datetime
    stock_item_id: Optional [str]
    stockItem: StockItemResponse  # Ensure this is the correct type

    class Config:
        from_attributes=True
        orm_mode = True


# Update
class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    brand_id: Optional[int] = None
    model_id: Optional[int] = None
    color_id: Optional[int] = None
    category_id: Optional[int] = None
    discount: Optional[float] = None
    rating: Optional[float] = None
    warranty: Optional[str] = None
    stock_status_id: Optional[int] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True

# This is the response schema that we send back to the client
class ProductUpdateResponse(BaseModel):
    id: int
    productcode: str
    title: str
    price: float
    description: Optional[str] = None
    brand_id: int
    model_id: int
    color_id: int
    category_id: int
    discount: float
    rating: Optional[float] = None
    warranty: Optional[str] = None
    stock_status_id: int
    image: Optional[str] = None
    created_at: Optional[datetime] = None  # Keep as datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True  # Allow using from_orm

    # Pydantic root validator to format the datetime fields
    @root_validator(pre=True)
    def format_dates(cls, values):
        # Check if values is a dictionary and format datetime fields
        if isinstance(values, dict):
            for field in ["created_at", "updated_at"]:
                if field in values and isinstance(values[field], datetime):
                    # Format the datetime into string in the desired format
                    values[field] = values[field].strftime("%Y-%m-%d %H:%M:%S")
        return values



