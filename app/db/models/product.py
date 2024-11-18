# app/db/models/product.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.config import Base
from datetime import datetime

from app.utility.utc import get_current_cambodia_time

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    productcode = Column(String, unique=True, index=True)
    title = Column(String)
    price = Column(Float)
    description = Column(String)
    brand_id = Column(Integer, ForeignKey("brands.id"), index=True)
    model_id = Column(Integer, ForeignKey("models.id"), index=True)
    color_id = Column(Integer, ForeignKey("colors.id"), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    discount = Column(Float, default=0)
    stockqty = Column(Integer, default=0)
    image = Column(String)
    rating = Column(Float, default=0)
    warranty = Column(String)
    stock_status_id = Column(Integer, ForeignKey('stock_status.id')) 
    stock_item_id = Column(String, ForeignKey('stocks.itemId'))

    created_at = Column(DateTime, default=get_current_cambodia_time)  
    updated_at = Column(DateTime, default=get_current_cambodia_time, onupdate=get_current_cambodia_time)  

    # Relationships
    stock_item = relationship("StockItem", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    model = relationship("Model", back_populates="products")
    color = relationship("Color", back_populates="products")
    category = relationship("Category", back_populates="products")
    stock_status = relationship("StockStatus", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, title='{self.title}', price={self.price})>"
