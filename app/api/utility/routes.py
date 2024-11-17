from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.inventory import StockStatusCreate
from app.schemas.utility import BrandCreate, BrandResponse, CategoryCreate, CategoryResponse, ColorCreate, ColorResponse, ModelCreate, ModelResponse, RoleCreateRequest, GenderCreateRequest, RoleResponse, GenderResponse, StatusResponse, SupplierCreate, SupplierResponse, UnitCreate, UnitResponse
from app.api.utility.controllers import create_brand, create_category, create_color, create_model, create_role, create_gender, create_stock_status, create_supplier, create_unit, get_all_genders, get_all_roles, get_brand, get_brands, get_categories, get_category, get_color, get_colors, get_gender_by_id, get_model, get_models, get_role_by_id, get_stock_status, get_stock_statuses, get_supplier, get_suppliers, get_unit, get_units

# Utility function to raise not found exception
def raise_not_found_exception(entity_name: str):
    raise HTTPException(status_code=404, detail=f"{entity_name} not found")

utility = APIRouter()

# Route for creating a new role
@utility.post("/role", response_model=RoleResponse)
def create_role_route(role_data: RoleCreateRequest, db: Session = Depends(get_db)):
    return create_role(role_data, db)

# Route for getting all roles
@utility.get("/roles", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return get_all_roles(db)

# Route for getting a single role by ID
@utility.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return get_role_by_id(role_id, db)

# Route for creating a new gender
@utility.post("/gender", response_model=GenderResponse)
def create_gender_route(gender_data: GenderCreateRequest, db: Session = Depends(get_db)):
    return create_gender(gender_data, db)

# Route for getting all genders
@utility.get("/genders", response_model=list[GenderResponse])
def get_genders(db: Session = Depends(get_db)):
    return get_all_genders(db)

# Route for getting a single gender by ID
@utility.get("/genders/{gender_id}", response_model=GenderResponse)
def get_gender(gender_id: int, db: Session = Depends(get_db)):
    return get_gender_by_id(gender_id, db)


# Brand Routes
@utility.post("/brand", response_model=BrandResponse)
def create_brand_endpoint(brand: BrandCreate, db: Session = Depends(get_db)):
    try:
        return create_brand(db=db, brand=brand)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/brands", response_model=List[BrandResponse])
def read_brands(db: Session = Depends(get_db)):
    return get_brands(db)

@utility.get("/brands/{brand_id}", response_model=BrandResponse)
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = get_brand(db, brand_id)
    if not brand:
        raise_not_found_exception("Brand")
    return brand


# Category Routes
@utility.post("/category", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(db=db, category=category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/categories", response_model=List[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@utility.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise_not_found_exception("Category")
    return category


# Color Routes
@utility.post("/color", response_model=ColorResponse)
def create_color_endpoint(color: ColorCreate, db: Session = Depends(get_db)):
    try:
        return create_color(db=db, color=color)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/colors", response_model=List[ColorResponse])
def read_colors(db: Session = Depends(get_db)):
    return get_colors(db)

@utility.get("/colors/{color_id}", response_model=ColorResponse)
def read_color(color_id: int, db: Session = Depends(get_db)):
    color = get_color(db, color_id)
    if not color:
        raise_not_found_exception("Color")
    return color


# Model Routes
@utility.post("/model", response_model=ModelResponse)
def create_model_endpoint(model: ModelCreate, db: Session = Depends(get_db)):
    try:
        return create_model(db=db, model=model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/models", response_model=List[ModelResponse])
def read_models(db: Session = Depends(get_db)):
    return get_models(db)

@utility.get("/models/{model_id}", response_model=ModelResponse)
def read_model(model_id: int, db: Session = Depends(get_db)):
    model = get_model(db, model_id)
    if not model:
        raise_not_found_exception("Model")
    return model


# StockStatus Routes
@utility.post("/status", response_model=StatusResponse)
def create_stock_status_endpoint(
    status: StockStatusCreate, db: Session = Depends(get_db)
):
    """
    Endpoint to create a new stock status.
    """
    try:
        return create_stock_status(db=db, status=status)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/statuses", response_model=List[StatusResponse])
def read_stock_statuses(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all stock statuses.
    """
    return get_stock_statuses(db)

@utility.get("/statuses/{status_id}", response_model=StatusResponse)
def read_stock_status(
    status_id: int, db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a stock status by ID.
    """
    return get_stock_status(db, status_id)


# Supplier Routes
@utility.post("/supplier", response_model=SupplierResponse)
def create_supplier_endpoint(supplier: SupplierCreate, db: Session = Depends(get_db)):
    try:
        return create_supplier(db=db, supplier=supplier)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@utility.get("/suppliers", response_model=List[SupplierResponse])
def read_suppliers(db: Session = Depends(get_db)):
    return get_suppliers(db)


@utility.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier(db, supplier_id)



# Unit Routes
@utility.post("/unit", response_model=UnitResponse)
def create_unit_endpoint(unit: UnitCreate, db: Session = Depends(get_db)):
    try:
        return create_unit(db=db, unit=unit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@utility.get("/units", response_model=List[UnitResponse])
def read_units(db: Session = Depends(get_db)):
    return get_units(db)

@utility.get("/units/{unit_id}", response_model=UnitResponse)
def read_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = get_unit(db, unit_id)
    if not unit:
        raise_not_found_exception("Unit")
    return unit