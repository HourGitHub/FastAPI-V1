# app/api/utility/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.utility.controllers import (
    create_brand, create_stock_status, delete_stock_status, get_brand, get_stock_status, update_brand, delete_brand,
    create_category, get_category, update_category, delete_category,
    create_color, get_color, update_color, delete_color,
    create_gender, get_gender, update_gender, delete_gender,
    create_model, get_model, update_model, delete_model,
    create_role, get_role, update_role, delete_role,
    create_supplier, get_supplier, update_stock_status, update_supplier, delete_supplier,
    create_unit, get_unit, update_unit, delete_unit
)
from app.schemas.utility import (
    BrandCreate, BrandResponse, CategoryCreate, CategoryResponse, ColorCreate, ColorResponse,
    GenderCreate, GenderResponse, ModelCreate, ModelResponse, RoleCreate, RoleResponse,
    StockStatusCreate, StockStatusResponse, SupplierCreate, SupplierResponse, UnitCreate, UnitResponse
)

utility_router = APIRouter()

# =====================
# Brand Endpoints
# =====================
@utility_router.post("/brands", response_model=BrandResponse)
def create_new_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return create_brand(db, brand)

@utility_router.get("/brands/{brand_id}", response_model=BrandResponse)
def get_single_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_brand(db, brand_id)

@utility_router.put("/brands/{brand_id}", response_model=BrandResponse)
def update_existing_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):
    return update_brand(db, brand_id, brand)

@utility_router.delete("/brands/{brand_id}")
def delete_existing_brand(brand_id: int, db: Session = Depends(get_db)):
    return delete_brand(db, brand_id)


# =====================
# Category Endpoints
# =====================
@utility_router.post("/categories", response_model=CategoryResponse)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

@utility_router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_single_category(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)

@utility_router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_existing_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    return update_category(db, category_id, category)

@utility_router.delete("/categories/{category_id}")
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)


# =====================
# Color Endpoints
# =====================
@utility_router.post("/colors", response_model=ColorResponse)
def create_new_color(color: ColorCreate, db: Session = Depends(get_db)):
    return create_color(db, color)

@utility_router.get("/colors/{color_id}", response_model=ColorResponse)
def get_single_color(color_id: int, db: Session = Depends(get_db)):
    return get_color(db, color_id)

@utility_router.put("/colors/{color_id}", response_model=ColorResponse)
def update_existing_color(color_id: int, color: ColorCreate, db: Session = Depends(get_db)):
    return update_color(db, color_id, color)

@utility_router.delete("/colors/{color_id}")
def delete_existing_color(color_id: int, db: Session = Depends(get_db)):
    return delete_color(db, color_id)


# =====================
# Gender Endpoints
# =====================
@utility_router.post("/genders", response_model=GenderResponse)
def create_new_gender(gender: GenderCreate, db: Session = Depends(get_db)):
    return create_gender(db, gender)

@utility_router.get("/genders/{gender_id}", response_model=GenderResponse)
def get_single_gender(gender_id: int, db: Session = Depends(get_db)):
    return get_gender(db, gender_id)

@utility_router.put("/genders/{gender_id}", response_model=GenderResponse)
def update_existing_gender(gender_id: int, gender: GenderCreate, db: Session = Depends(get_db)):
    return update_gender(db, gender_id, gender)

@utility_router.delete("/genders/{gender_id}")
def delete_existing_gender(gender_id: int, db: Session = Depends(get_db)):
    return delete_gender(db, gender_id)


# =====================
# Model Endpoints
# =====================
@utility_router.post("/models", response_model=ModelResponse)
def create_new_model(model: ModelCreate, db: Session = Depends(get_db)):
    return create_model(db, model)

@utility_router.get("/models/{model_id}", response_model=ModelResponse)
def get_single_model(model_id: int, db: Session = Depends(get_db)):
    return get_model(db, model_id)

@utility_router.put("/models/{model_id}", response_model=ModelResponse)
def update_existing_model(model_id: int, model: ModelCreate, db: Session = Depends(get_db)):
    return update_model(db, model_id, model)

@utility_router.delete("/models/{model_id}")
def delete_existing_model(model_id: int, db: Session = Depends(get_db)):
    return delete_model(db, model_id)


# =====================
# Role Endpoints
# =====================
@utility_router.post("/roles", response_model=RoleResponse)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)

@utility_router.get("/roles/{role_id}", response_model=RoleResponse)
def get_single_role(role_id: int, db: Session = Depends(get_db)):
    return get_role(db, role_id)

@utility_router.put("/roles/{role_id}", response_model=RoleResponse)
def update_existing_role(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    return update_role(db, role_id, role)

@utility_router.delete("/roles/{role_id}")
def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
    return delete_role(db, role_id)


# =====================
# Status Endpoints
# =====================
@utility_router.post("/stock-statuses", response_model=StockStatusResponse)
def create_new_stock_status(stock_status: StockStatusCreate, db: Session = Depends(get_db)):
    return create_stock_status(db, stock_status)

@utility_router.get("/stock-statuses/{stock_status_id}", response_model=StockStatusResponse)
def get_single_stock_status(stock_status_id: int, db: Session = Depends(get_db)):
    return get_stock_status(db, stock_status_id)

@utility_router.put("/stock-statuses/{stock_status_id}", response_model=StockStatusResponse)
def update_existing_stock_status(stock_status_id: int, stock_status: StockStatusCreate, db: Session = Depends(get_db)):
    return update_stock_status(db, stock_status_id, stock_status)

@utility_router.delete("/stock-statuses/{stock_status_id}")
def delete_existing_stock_status(stock_status_id: int, db: Session = Depends(get_db)):
    return delete_stock_status(db, stock_status_id)


# =====================
# Supplier Endpoints
# =====================
@utility_router.post("/suppliers", response_model=SupplierResponse)
def create_new_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db, supplier)

@utility_router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
def get_single_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier(db, supplier_id)

@utility_router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_existing_supplier(supplier_id: int, supplier: SupplierCreate, db: Session = Depends(get_db)):
    return update_supplier(db, supplier_id, supplier)

@utility_router.delete("/suppliers/{supplier_id}")
def delete_existing_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier(db, supplier_id)


# =====================
# Unit Endpoints
# =====================
@utility_router.post("/units", response_model=UnitResponse)
def create_new_unit(unit: UnitCreate, db: Session = Depends(get_db)):
    return create_unit(db, unit)

@utility_router.get("/units/{unit_id}", response_model=UnitResponse)
def get_single_unit(unit_id: int, db: Session = Depends(get_db)):
    return get_unit(db, unit_id)

@utility_router.put("/units/{unit_id}", response_model=UnitResponse)
def update_existing_unit(unit_id: int, unit: UnitCreate, db: Session = Depends(get_db)):
    return update_unit(db, unit_id, unit)

@utility_router.delete("/units/{unit_id}")
def delete_existing_unit(unit_id: int, db: Session = Depends(get_db)):
    return delete_unit(db, unit_id)
