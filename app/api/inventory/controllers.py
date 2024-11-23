from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.utility import StockStatus
from app.db.models.inventory import StockItem
from app.schemas.inventory import Product, StockItemResponse, StockItemUpdate
import logging

from app.utility.telegramAlert import send_telegram_message


logger = logging.getLogger(__name__)

def create_stock_item(db: Session, product: Product) -> StockItemResponse:
    """Create a new stock item."""
    stock_item_data = product.dict(exclude_unset=True)

    stock_status_id = stock_item_data.get('statusId')
    if not stock_status_id:
        logger.error("Missing statusId in the request payload.")
        send_telegram_message("🚨 Error: Missing statusId in the request payload for creating a stock item.")
        raise HTTPException(status_code=400, detail="Missing statusId.")

    if db.query(StockItem).filter(StockItem.itemId == product.itemId).first():
        logger.error("Duplicate itemId: %s", product.itemId)
        send_telegram_message(f"🚨 Error: Duplicate itemId {product.itemId} - This itemId already exists.")
        raise HTTPException(status_code=400, detail="Duplicate itemId: This itemId already exists.")

    stock_status = db.query(StockStatus).filter(StockStatus.id == stock_status_id).first()
    if not stock_status:
        logger.error("Invalid statusId: %s", stock_status_id)
        send_telegram_message(f"🚨 Error: Invalid statusId {stock_status_id} when creating stock item.")
        raise HTTPException(status_code=400, detail="Invalid statusId.")

    db_stock_item = StockItem(
        itemId=product.itemId,
        item_name=product.itemName,
        category_id=product.categoryId,
        unit_id=product.unitId,
        quantity_added=product.quantityAdded,
        quantity_in_stock=product.quantityInStock,
        purchase_date=product.purchaseDate,
        purchase_price=product.purchasePrice,
        expiry_date=product.expiryDate,
        barcode=product.barcode,
        remark=product.remark,
        restock_level=product.restockLevel,
        supplier_id=product.supplierId,
        stock_status_id=stock_status_id,
        image=product.image,
    )

    try:
        db.add(db_stock_item)
        db.commit()
        db.refresh(db_stock_item)
        logger.info("Created stock item: %s", db_stock_item.itemId)
    except Exception as e:
        db.rollback()
        logger.error("Error creating stock item: %s", e)
        send_telegram_message(f"🚨 Error creating stock item: {e}")
        raise HTTPException(status_code=500, detail="Database error while creating stock item.")

    return _generate_stock_item_response(db_stock_item, db)


def _generate_stock_item_response(db_stock_item: StockItem, db: Session) -> StockItemResponse:
    """Generate a response model for the StockItem."""
    category = db_stock_item.category
    unit = db_stock_item.unit
    supplier = db_stock_item.supplier
    stock_status = db_stock_item.stock_status

    return StockItemResponse(
        id=db_stock_item.id,
        item_id=db_stock_item.itemId,
        item_name=db_stock_item.item_name,
        category_name=category.name if category else "Unknown",
        unit_name=unit.name if unit else "Unknown",
        quantity_added=db_stock_item.quantity_added,
        quantity_in_stock=db_stock_item.quantity_in_stock,
        purchase_date=db_stock_item.purchase_date,
        purchase_price=db_stock_item.purchase_price,
        expiry_date=db_stock_item.expiry_date,
        barcode=db_stock_item.barcode,
        remark=db_stock_item.remark,
        restock_level=db_stock_item.restock_level,
        supplier_name=supplier.name if supplier else "Unknown",
        status=stock_status.name if stock_status else "Unknown",
        timestamp=db_stock_item.created_at,
        image=db_stock_item.image
    )


def update_stock_item(db: Session, item_id: int, stock_item: StockItemUpdate) -> StockItemResponse:
    """Update an existing stock item."""
    db_stock_item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not db_stock_item:
        logger.error("Stock item not found for ID: %d", item_id)
        send_telegram_message(f"🚨 Error: Stock item not found for ID: {item_id} during update.")
        raise HTTPException(status_code=404, detail="Stock item not found.")

    update_data = stock_item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_stock_item, key, value)

    try:
        db.commit()
        db.refresh(db_stock_item)
        logger.info("Updated stock item ID: %d", item_id)
    except Exception as e:
        db.rollback()
        logger.error("Error updating stock item ID %d: %s", item_id, e)
        send_telegram_message(f"🚨 Error updating stock item ID: {item_id} - {e}")
        raise HTTPException(status_code=500, detail="Error updating stock item.")
    
    return _generate_stock_item_response(db_stock_item, db)


def get_all_stock_items(db: Session) -> List[StockItemResponse]:
    """Retrieve all stock items."""
    stock_items = db.query(StockItem).all()
    return [_generate_stock_item_response(item, db) for item in stock_items]


def get_stock_item(db: Session, item_id: int) -> StockItemResponse:
    """Retrieve a stock item by its ID."""
    stock_item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not stock_item:
        logger.error("Stock item not found for ID: %d", item_id)
        send_telegram_message(f"🚨 Error: Stock item not found for ID: {item_id} when retrieving stock item.")
        raise HTTPException(status_code=404, detail="Stock item not found.")
    
    return _generate_stock_item_response(stock_item, db)


def delete_stock_item(db: Session, stock_item_id: int):
    """Delete a stock item by its ID."""
    stock_item = db.query(StockItem).filter(StockItem.id == stock_item_id).first()
    if not stock_item:
        logger.error("Stock item not found for ID: %d", stock_item_id)
        send_telegram_message(f"🚨 Error: Stock item not found for ID: {stock_item_id} during deletion.")
        raise HTTPException(status_code=404, detail="Stock item not found.")
    
    try:
        db.delete(stock_item)
        db.commit()
        logger.info("Deleted stock item ID: %d", stock_item_id)
        return {"message": "Stock item deleted successfully.", "status": 200}
    except Exception as e:
        db.rollback()
        logger.error("Error deleting stock item ID %d: %s", stock_item_id, e)
        send_telegram_message(f"🚨 Error deleting stock item ID: {stock_item_id} - {e}")
        raise HTTPException(status_code=500, detail="Error deleting stock item.")


def get_stock_status(db: Session, item_id: int):
    """Retrieve the stock status for a given item."""
    stock_item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not stock_item:
        logger.error("Stock item not found for ID: %d", item_id)
        send_telegram_message(f"🚨 Error: Stock item not found for ID: {item_id} when retrieving stock status.")
        raise HTTPException(status_code=404, detail="Stock item not found.")

    return {
        "available": stock_item.quantity_in_stock,
        "out_of_stock": 1 if stock_item.quantity_in_stock == 0 else 0,
        "status": 200
    }
