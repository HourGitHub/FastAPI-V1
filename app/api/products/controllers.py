from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query
from app.api.products.helper import apply_filters, build_product_response, get_related_models
from app.db.models.product import Product
from app.db.models.utility import Brand, Model, Color, Category, StockStatus
from app.db.models.inventory import StockItem
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductUpdateResponse, StockItemResponse
from app.db.config import get_db  
from app.utility.telegramAlert import send_telegram_message

# Create Product
def create_product(db: Session, product: ProductCreate):
    try:
        # Check if the product already exists
        existing_product = db.query(Product).filter(Product.productcode == product.productcode).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product with this productcode already exists.")
        
        # Create a new product
        db_product = Product(
            productcode=product.productcode,
            title=product.title,
            price=product.price,
            description=product.description,
            brand_id=product.brand_id,
            model_id=product.model_id,
            color_id=product.color_id,
            category_id=product.category_id,
            discount=product.discount,
            rating=product.rating,
            warranty=product.warranty,
            stock_status_id=product.status_id,
            image=product.image,
            stock_item_id=product.stockItemId,  # Ensure this is passed as string if `itemId` is a string
        )
        
        # Add to session and commit to DB
        db.add(db_product)
        db.commit()
        db.refresh(db_product)  # Refresh to get the id and updated fields

        # Get the related models
        brand = db.query(Brand).filter(Brand.id == db_product.brand_id).first()
        model = db.query(Model).filter(Model.id == db_product.model_id).first()
        color = db.query(Color).filter(Color.id == db_product.color_id).first()
        category = db.query(Category).filter(Category.id == db_product.category_id).first()
        status = db.query(StockStatus).filter(StockStatus.id == db_product.stock_status_id).first()
        stock_item = db.query(StockItem).filter(StockItem.itemId == db_product.stock_item_id).first()

        # Validate that the related models exist
        if not (brand and model and color and category and status and stock_item):
            raise HTTPException(status_code=400, detail="Invalid foreign key references")

        # Convert expiry_date to string if it's a datetime object
        expiry_date_str = stock_item.expiry_date.isoformat() if stock_item.expiry_date else None

        # Prepare response, using `name` fields instead of `id` for related models
        return ProductResponse(
            id=db_product.id,
            productcode=db_product.productcode,
            title=db_product.title,
            price=db_product.price,
            description=db_product.description,
            brand_name=brand.name,  # Return `name` of `Brand`
            model_name=model.name,  # Return `name` of `Model`
            color_name=color.name,  # Return `name` of `Color`
            category_name=category.name,  # Return `name` of `Category`
            discount=db_product.discount,
            rating=db_product.rating,
            warranty=db_product.warranty,
            stock_status_name=status.name,  # Return `name` of `StockStatus`
            image=db_product.image,
            created_at=db_product.created_at,
            stock_item_id=stock_item.itemId,  # Return itemId as string
            stockItem=StockItemResponse(
                itemId=stock_item.itemId,
                itemName=stock_item.item_name,
                quantityInStock=stock_item.quantity_in_stock,
                expiryDate=expiry_date_str,  # Use the string representation of the datetime
                unitName=stock_item.unit.name if stock_item.unit else None,
                categoryName=stock_item.category.name if stock_item.category else None,
                status=stock_item.stock_status.name if stock_item.stock_status else None,
                barcode=stock_item.barcode
            )
        )
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Update Product
def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    try:
        # Fetch the product by ID
        db_product = db.query(Product).filter(Product.id == product_id).first()

        # If product not found, raise a 404 error
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Update the fields if provided in the request body
        if product_data.title is not None:
            db_product.title = product_data.title
        if product_data.price is not None:
            db_product.price = product_data.price
        if product_data.description is not None:
            db_product.description = product_data.description
        if product_data.brand_id is not None:
            db_product.brand_id = product_data.brand_id
        if product_data.model_id is not None:
            db_product.model_id = product_data.model_id
        if product_data.color_id is not None:
            db_product.color_id = product_data.color_id
        if product_data.category_id is not None:
            db_product.category_id = product_data.category_id
        if product_data.discount is not None:
            db_product.discount = product_data.discount
        if product_data.rating is not None:
            db_product.rating = product_data.rating
        if product_data.warranty is not None:
            db_product.warranty = product_data.warranty
        if product_data.stock_status_id is not None:
            db_product.stock_status_id = product_data.stock_status_id
        if product_data.image is not None:
            db_product.image = product_data.image

        # Set the current time as the new updated_at value
        db_product.updated_at = datetime.now()

        # Commit the changes to the database
        db.commit()
        db.refresh(db_product)

        # Return the updated product as a response
        return ProductUpdateResponse.from_orm(db_product)

    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error updating product ID {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get all products
def get_all_products(db: Session):
    try:
        # Fetch all products from the database
        db_products = db.query(Product).all()

        # If no products found, raise a 404 error
        if not db_products:
            raise HTTPException(status_code=404, detail="No products found.")

        # Prepare the response with all product details
        products = []
        for db_product in db_products:
            # Fetch related models (brand, model, color, category, stock status, stock item)
            brand, model, color, category, status, stock_item = get_related_models(db, db_product)

            # Append product details to the response list
            products.append(build_product_response(db_product, brand, model, color, category, status, stock_item))

        return products
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error fetching all products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get single product
def get_single_product(db: Session, product_id: int):
    try:
        # Fetch the product by ID from the database
        db_product = db.query(Product).filter(Product.id == product_id).first()

        # If the product is not found, raise a 404 error
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Fetch related models (brand, model, color, category, stock status, stock item)
        brand, model, color, category, status, stock_item = get_related_models(db, db_product)

        # Return the product details as a response
        return build_product_response(db_product, brand, model, color, category, status, stock_item)
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error fetching product ID {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Limit products (pagination or limit fetch)
def get_limited_products(db: Session, limit: int = Query(10, ge=1)):
    try:
        # Fetch the limited number of products from the database
        db_products = db.query(Product).limit(limit).all()

        # If no products found, raise a 404 error
        if not db_products:
            raise HTTPException(status_code=404, detail="No products found.")

        # Prepare the response with all product details
        products = []
        for db_product in db_products:
            # Fetch related models (brand, model, color, category, stock status, stock item)
            brand, model, color, category, status, stock_item = get_related_models(db, db_product)

            # Append product details to the response list
            products.append(build_product_response(db_product, brand, model, color, category, status, stock_item))

        return products
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error fetching limited products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Search products (with filters and sorting)
def search_products(
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
    sort_by: str = None,  # Sorting parameter
    sort_order: str = 'asc'  # Sorting order
):
    try:
        # Apply filters using the helper function
        query = apply_filters(
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
            sort_by=sort_by,  # Pass sorting parameters
            sort_order=sort_order
        )

        # Fetch results
        db_products = query.all()

        # If no products found, raise a 404 error
        if not db_products:
            raise HTTPException(status_code=404, detail="No products found.")

        # Prepare response for all found products
        products = []
        for db_product in db_products:
            # Fetch related models (brand, model, color, category, stock status, stock item)
            brand, model, color, category, status, stock_item = get_related_models(db, db_product)

            # Append product details to the response list
            products.append(build_product_response(db_product, brand, model, color, category, status, stock_item))

        return products
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error searching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Delete Product
def delete_product(db: Session, product_id: int):
    try:
        # Fetch the product by ID
        db_product = db.query(Product).filter(Product.id == product_id).first()

        # If product not found, raise a 404 error
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Delete the product from the database
        db.delete(db_product)
        db.commit()

        # Send Telegram message upon deletion
        send_telegram_message(f"🗑️ Product deleted: {db_product.productcode} - {db_product.title}.")

        # Return a success message or a status code
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error deleting product ID {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Delete multiple products
def delete_multiple_products(db: Session, product_ids: list[int]):
    try:
        # Fetch the products with the given IDs from the database
        products_to_delete = db.query(Product).filter(Product.id.in_(product_ids)).all()

        # If no products are found, raise an error
        if not products_to_delete:
            raise HTTPException(status_code=404, detail="No products found with the provided IDs")

        # Delete the products
        for product in products_to_delete:
            db.delete(product)

        # Commit the transaction
        db.commit()

        # Send Telegram message upon deletion
        send_telegram_message(f"🗑️ {len(products_to_delete)} products deleted: {', '.join([p.productcode for p in products_to_delete])}.")
        # Return a success message
        return {"detail": f"{len(products_to_delete)} products deleted successfully"}
    except Exception as e:
        # Send Telegram message only in case of an error
        send_telegram_message(f"❌ Error deleting multiple products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
