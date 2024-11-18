# app/db/models/inventory.py

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.config import Base
from sqlalchemy import func
from app.db.models.product import Product 

from app.utility.utc import get_current_cambodia_time

class StockItem(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, index=True)
    itemId = Column(String, unique=True, nullable=False)
    item_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    unit_id = Column(Integer, ForeignKey('units.id'))
    quantity_added = Column(Integer, default=0)
    quantity_in_stock = Column(Integer, default=0)
    purchase_date = Column(DateTime, default=func.now())
    purchase_price = Column(Float, default=0.0)
    expiry_date = Column(DateTime, nullable=True)
    barcode = Column(String, nullable=True, default="")
    remark = Column(String, nullable=True, default="")
    restock_level = Column(Integer, default=0)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    stock_status_id = Column(Integer, ForeignKey("stock_status.id"), nullable=False)
    image = Column(String, nullable=True, default="")
    
    created_at = Column(DateTime, default=get_current_cambodia_time)  
    updated_at = Column(DateTime, default=get_current_cambodia_time, onupdate=get_current_cambodia_time)  

    # Relationships
    category = relationship("Category", back_populates="stocks")
    unit = relationship("Unit", back_populates="stocks")
    supplier = relationship("Supplier", back_populates="stocks")
    stock_status = relationship("StockStatus", back_populates="stock_items")
    products = relationship("Product", back_populates="stock_item")

    def __repr__(self):
        status = self.stock_status.name if self.stock_status else "Unknown"
        return f"<StockItem(id={self.id}, item_name='{self.item_name}', itemId='{self.itemId}', status='{status}')>"

    __table_args__ = (
        Index('ix_stocks_itemId', 'itemId'),
        Index('ix_stocks_category_id', 'category_id'),
        Index('ix_stocks_supplier_id', 'supplier_id'),
    )
