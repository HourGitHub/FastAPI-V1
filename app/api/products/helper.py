# app/api/products/helper.py

from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.db.models.utility import Brand, Model, Color, Category, StockStatus
from app.db.models.inventory import StockItem
from app.schemas.product import ProductResponse, StockItemResponse
from fastapi import HTTPException

# Helper function to get related models for a product
def get_related_models(db: Session, db_product: Product):
    brand = db.query(Brand).filter(Brand.id == db_product.brand_id).first()
    model = db.query(Model).filter(Model.id == db_product.model_id).first()
    color = db.query(Color).filter(Color.id == db_product.color_id).first()
    category = db.query(Category).filter(Category.id == db_product.category_id).first()
    status = db.query(StockStatus).filter(StockStatus.id == db_product.stock_status_id).first()
    stock_item = db.query(StockItem).filter(StockItem.itemId == db_product.stock_item_id).first()

    # Validate that all related models exist
    if not (brand and model and color and category and status and stock_item):
        raise HTTPException(status_code=400, detail="Invalid foreign key references")

    return brand, model, color, category, status, stock_item

# Helper function to build the response for a product and its stock item
def build_product_response(db_product: Product, brand, model, color, category, status, stock_item):
    # Convert expiry_date to string if it's a datetime object
    expiry_date_str = stock_item.expiry_date.isoformat() if stock_item.expiry_date else None

    return ProductResponse(
        id=db_product.id,
        productcode=db_product.productcode,
        title=db_product.title,
        price=db_product.price,
        description=db_product.description,
        brand_name=brand.name,
        model_name=model.name,
        color_name=color.name,
        category_name=category.name,
        discount=db_product.discount,
        rating=db_product.rating,
        warranty=db_product.warranty,
        stock_status_name=status.name,
        image=db_product.image,
        created_at=db_product.created_at,
        stock_item_id=stock_item.itemId,
        stockItem=StockItemResponse(
            itemId=stock_item.itemId,
            itemName=stock_item.item_name,
            quantityInStock=stock_item.quantity_in_stock,
            expiryDate=expiry_date_str,
            unitName=stock_item.unit.name if stock_item.unit else None,
            categoryName=stock_item.category.name if stock_item.category else None,
            status=stock_item.stock_status.name if stock_item.stock_status else None,
            barcode=stock_item.barcode
        )
    )

# Helper function to search
def apply_filters(
    db: Session, 
    id: int = None, 
    title: str = None, 
    min_price: float = None, 
    max_price: float = None,
    category_name: str = None,
    model_name: str = None,
    brand_name: str = None,
    color_name: str = None,
    stock_status_name: str = None,
    productcode: str = None,
    sort_by: str = None,  # New parameter for sorting
    sort_order: str = 'asc'  # New parameter for sort direction (default is 'asc')
):
    query = db.query(Product)

    # Filter by id if provided
    if id:
        query = query.filter(Product.id == id)
    
    # Filter by title if provided (case-insensitive partial match)
    if title:
        query = query.filter(Product.title.ilike(f"%{title}%"))
    
    # Filter by price range if provided
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Filter by category name if provided
    if category_name:
        query = query.join(Category).filter(Category.name.ilike(f"%{category_name}%"))
    
    # Filter by model name if provided
    if model_name:
        query = query.join(Model).filter(Model.name.ilike(f"%{model_name}%"))
    
    # Filter by brand name if provided
    if brand_name:
        query = query.join(Brand).filter(Brand.name.ilike(f"%{brand_name}%"))
    
    # Filter by color name if provided
    if color_name:
        query = query.join(Color).filter(Color.name.ilike(f"%{color_name}%"))
    
    # Filter by stock status name if provided
    if stock_status_name:
        query = query.join(StockStatus).filter(StockStatus.name.ilike(f"%{stock_status_name}%"))
    
    # Filter by product code if provided
    if productcode:
        query = query.filter(Product.productcode.ilike(f"%{productcode}%"))

    # Sort products if sort_by is provided
    if sort_by:
        if sort_by == 'price':
            query = query.order_by(Product.price)
        elif sort_by == 'title':
            query = query.order_by(Product.title)
        elif sort_by == 'rating':
            query = query.order_by(Product.rating)
        elif sort_by == 'created_at':
            query = query.order_by(Product.created_at)
        else:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        # Apply sort direction (ascending or descending)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_by))

    return query