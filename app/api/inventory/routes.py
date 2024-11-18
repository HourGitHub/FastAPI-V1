# app/api/inventory/routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.inventory import Product, StockItemResponse, ErrorResponse, StockItemUpdate
from app.api.inventory.controllers import (
    create_stock_item,
    delete_stock_item,
    get_all_stock_items,
    get_stock_item,
    get_stock_status,
    update_stock_item,
)
from app.db.config import get_db
import logging

logger = logging.getLogger(__name__)

stock = APIRouter()

@stock.post("/stocks", response_model=StockItemResponse, responses={400: {"model": ErrorResponse}})
def create_stock(stock_item_request: Product, db: Session = Depends(get_db)):
    try:
        return create_stock_item(db=db, product=stock_item_request)
    except HTTPException as e:
        logger.error(f"Error creating stock item: {e.detail}")
        raise e

@stock.get("/stocks", response_model=List[StockItemResponse])
def read_stocks(db: Session = Depends(get_db)):
    try:
        return get_all_stock_items(db)
    except Exception as e:
        logger.error(f"Error fetching all stock items: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching stock items")

@stock.get("/stocks/{item_id}", response_model=StockItemResponse)
def read_stock(item_id: int, db: Session = Depends(get_db)):
    try:
        return get_stock_item(db, item_id)
    except HTTPException as e:
        logger.error(f"Error fetching stock item by ID {item_id}: {e.detail}")
        raise e

@stock.put("/stocks/{item_id}", response_model=StockItemResponse, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
def update_stock(item_id: int, stock_item: StockItemUpdate, db: Session = Depends(get_db)):
    try:
        return update_stock_item(db=db, item_id=item_id, stock_item=stock_item)
    except HTTPException as e:
        logger.error(f"Error updating stock item ID {item_id}: {e.detail}")
        raise e

@stock.delete("/stocks/{id}", status_code=200)
def delete_stock(id: int, db: Session = Depends(get_db)):
    try:
        return delete_stock_item(db, id)
    except HTTPException as e:
        logger.error(f"Error deleting stock item ID {id}: {e.detail}")
        raise e

@stock.get("/stocks/status/{item_id}", response_model=dict)
def stock_status(item_id: int, db: Session = Depends(get_db)):
    try:
        return get_stock_status(db=db, item_id=item_id)
    except HTTPException as e:
        logger.error(f"Error fetching stock status for item ID {item_id}: {e.detail}")
        raise e
