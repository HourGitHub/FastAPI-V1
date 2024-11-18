# app/api/products/routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductUpdateResponse
from app.api.products.controllers import create_product, delete_multiple_products, delete_product, get_all_products, get_limited_products, get_single_product, search_products, update_product
from app.db.config import get_db  
from sqlalchemy.orm import Session


products = APIRouter()

@products.post("/products/", response_model=ProductResponse)
def create_product_route(
    product: ProductCreate, db: Session = Depends(get_db)
):
    try:
        return create_product(db=db, product=product)
    except HTTPException as e:
        raise e


@products.put("/products/{product_id}", response_model=ProductUpdateResponse)
def update_product_route(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db=db, product_id=product_id, product_data=product_data)

@products.get("/products/", response_model=List[ProductResponse])
def get_products_route(db: Session = Depends(get_db)):
    return get_all_products(db=db)
    
    
@products.get("/products/{product_id}", response_model=ProductResponse)
def get_product_route(product_id: int, db: Session = Depends(get_db)):
    return get_single_product(db=db, product_id=product_id)

@products.get("/limit/products/", response_model=List[ProductResponse])
def get_limited_products_route(
    limit: int = Query(10, ge=1), db: Session = Depends(get_db)
):
    try:
        return get_limited_products(db=db, limit=limit)
    except HTTPException as e:
        raise e

@products.get("/products/search/", response_model=List[ProductResponse])
def search_products_route(
    id: int = Query(None, ge=1),  # Optional product ID
    title: str = Query(None),  # Optional title search
    min_price: float = Query(None),  # Optional minimum price
    max_price: float = Query(None),  # Optional maximum price
    category_name: str = Query(None),  # Optional category name
    model_name: str = Query(None),  # Optional model name
    brand_name: str = Query(None),  # Optional brand name
    color_name: str = Query(None),  # Optional color name
    stock_status_name: str = Query(None),  # Optional stock status name
    productcode: str = Query(None),  # Optional product code
    sort_by: str = Query(None, regex="^(price|title|rating|created_at)$"),  # Sort field
    sort_order: str = Query('asc', regex="^(asc|desc)$"),  # Sort order (default is 'asc')
    db: Session = Depends(get_db)
):
    try:
        return search_products(
            db=db,
            id=id,
            title=title,
            min_price=min_price,
            max_price=max_price,
            category_name=category_name,
            model_name=model_name,
            brand_name=brand_name,
            color_name=color_name,
            stock_status_name=stock_status_name,
            productcode=productcode,
            sort_by=sort_by,  # Include sorting params in the query
            sort_order=sort_order
        )
    except HTTPException as e:
        raise e
    
# DELETE 
@products.delete("/products/{product_id}", response_model=dict)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product(db=db, product_id=product_id)
    except HTTPException as e:
        raise e
    

# DELETE route to delete multiple products by IDs (sent as query parameters)
@products.delete("/products/", response_model=dict)
def delete_multiple_products_route(
    product_ids: list[int] = Query(...),  # List of product IDs passed as query parameters
    db: Session = Depends(get_db)
):
    try:
        return delete_multiple_products(db=db, product_ids=product_ids)
    except HTTPException as e:
        raise e