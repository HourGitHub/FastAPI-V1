# app/api/utility/controllers.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Brand, Category, Color, Gender, Model, Role, StockStatus, Supplier, Unit
from app.schemas.utility import (
    BrandCreate, CategoryCreate, ColorCreate, GenderCreate, ModelCreate, RoleCreate, StockStatusCreate, SupplierCreate, UnitCreate
)

# Common CRUD utilities
def get_item(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item

def create_item(db: Session, model, schema):
    new_item = model(**schema.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_item(db: Session, model, item_id: int, schema):
    item = get_item(db, model, item_id)
    for key, value in schema.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, model, item_id: int):
    item = get_item(db, model, item_id)
    db.delete(item)
    db.commit()
    return {"message": f"{model.__name__} deleted successfully"}

# Specific functions for each entity

# =====================
# Brand
# =====================
def create_brand(db: Session, brand: BrandCreate):
    return create_item(db, Brand, brand)

def get_brand(db: Session, brand_id: int):
    return get_item(db, Brand, brand_id)

def update_brand(db: Session, brand_id: int, brand: BrandCreate):
    return update_item(db, Brand, brand_id, brand)

def delete_brand(db: Session, brand_id: int):
    return delete_item(db, Brand, brand_id)


# =====================
# Category
# =====================
def create_category(db: Session, category: CategoryCreate):
    return create_item(db, Category, category)

def get_category(db: Session, category_id: int):
    return get_item(db, Category, category_id)

def update_category(db: Session, category_id: int, category: CategoryCreate):
    return update_item(db, Category, category_id, category)

def delete_category(db: Session, category_id: int):
    return delete_item(db, Category, category_id)


# =====================
# Color
# =====================
def create_color(db: Session, color: ColorCreate):
    return create_item(db, Color, color)

def get_color(db: Session, color_id: int):
    return get_item(db, Color, color_id)

def update_color(db: Session, color_id: int, color: ColorCreate):
    return update_item(db, Color, color_id, color)

def delete_color(db: Session, color_id: int):
    return delete_item(db, Color, color_id)


# =====================
# Gender
# =====================
def create_gender(db: Session, gender: GenderCreate):
    return create_item(db, Gender, gender)

def get_gender(db: Session, gender_id: int):
    return get_item(db, Gender, gender_id)

def update_gender(db: Session, gender_id: int, gender: GenderCreate):
    return update_item(db, Gender, gender_id, gender)

def delete_gender(db: Session, gender_id: int):
    return delete_item(db, Gender, gender_id)


# =====================
# Model
# =====================
def create_model(db: Session, model: ModelCreate):
    return create_item(db, Model, model)

def get_model(db: Session, model_id: int):
    return get_item(db, Model, model_id)

def update_model(db: Session, model_id: int, model: ModelCreate):
    return update_item(db, Model, model_id, model)

def delete_model(db: Session, model_id: int):
    return delete_item(db, Model, model_id)


# =====================
# Role
# =====================
def create_role(db: Session, role: RoleCreate):
    return create_item(db, Role, role)

def get_role(db: Session, role_id: int):
    return get_item(db, Role, role_id)

def update_role(db: Session, role_id: int, role: RoleCreate):
    return update_item(db, Role, role_id, role)

def delete_role(db: Session, role_id: int):
    return delete_item(db, Role, role_id)


# =====================
# Status
# =====================
def create_stock_status(db: Session, stock_status: StockStatusCreate):
    db_stock_status = StockStatus(name=stock_status.name, description=stock_status.description)
    db.add(db_stock_status)
    db.commit()
    db.refresh(db_stock_status)
    return db_stock_status

def get_stock_status(db: Session, stock_status_id: int):
    return db.query(StockStatus).filter(StockStatus.id == stock_status_id).first()

def update_stock_status(db: Session, stock_status_id: int, stock_status: StockStatusCreate):
    db_stock_status = db.query(StockStatus).filter(StockStatus.id == stock_status_id).first()
    if db_stock_status:
        db_stock_status.name = stock_status.name
        db_stock_status.description = stock_status.description
        db.commit()
        db.refresh(db_stock_status)
    return db_stock_status

def delete_stock_status(db: Session, stock_status_id: int):
    db_stock_status = db.query(StockStatus).filter(StockStatus.id == stock_status_id).first()
    if db_stock_status:
        db.delete(db_stock_status)
        db.commit()
    return db_stock_status


# =====================
# Supplier
# =====================
def create_supplier(db: Session, supplier: SupplierCreate):
    return create_item(db, Supplier, supplier)

def get_supplier(db: Session, supplier_id: int):
    return get_item(db, Supplier, supplier_id)

def update_supplier(db: Session, supplier_id: int, supplier: SupplierCreate):
    return update_item(db, Supplier, supplier_id, supplier)

def delete_supplier(db: Session, supplier_id: int):
    return delete_item(db, Supplier, supplier_id)


# =====================
# Unit
# =====================
def create_unit(db: Session, unit: UnitCreate):
    return create_item(db, Unit, unit)

def get_unit(db: Session, unit_id: int):
    return get_item(db, Unit, unit_id)

def update_unit(db: Session, unit_id: int, unit: UnitCreate):
    return update_item(db, Unit, unit_id, unit)

def delete_unit(db: Session, unit_id: int):
    return delete_item(db, Unit, unit_id)
