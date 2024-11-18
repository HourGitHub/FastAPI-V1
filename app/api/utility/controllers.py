# app/api/utility/controllers.py
from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Role, Gender
from app.db.models.utility import Brand, Category, Color, Model, StockStatus, Supplier, Unit
from app.schemas.inventory import StockStatusCreate
from app.schemas.utility import BrandCreate, BrandResponse, CategoryCreate, CategoryResponse, ColorCreate, ColorResponse, ContactInfo, ModelCreate, ModelResponse, RoleCreateRequest, RoleResponse, GenderCreateRequest, GenderResponse, StatusResponse, SupplierCreate, SupplierResponse, UnitCreate, UnitResponse
from app.core.logging import logger



# =======================
# Brand Controller
# =======================
def create_brand(db: Session, brand: BrandCreate) -> BrandResponse:
    check_existing_entity(db, Brand, brand.name, "Brand")
    db_brand = Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    logger.info(f"Brand created: {brand.name}")
    return BrandResponse.from_orm(db_brand)

def get_brands(db: Session, skip: int = 0, limit: int = 10) -> List[BrandResponse]:
    brands = db.query(Brand).offset(skip).limit(limit).all()
    return [BrandResponse.from_orm(brand) for brand in brands]

def get_brand(db: Session, brand_id: int) -> BrandResponse:
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return BrandResponse.from_orm(brand)

# =======================
# Category Controller
# =======================
def create_category(db: Session, category: CategoryCreate) -> CategoryResponse:
    check_existing_entity(db, Category, category.name, "Category")
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    logger.info(f"Category created: {category.name}")
    return CategoryResponse.from_orm(db_category)

def get_categories(db: Session) -> List[CategoryResponse]:
    return [CategoryResponse.from_orm(category) for category in db.query(Category).all()]

def get_category(db: Session, category_id: int) -> CategoryResponse:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse.from_orm(category)


# =======================
# Color Controller
# =======================
def create_color(db: Session, color: ColorCreate) -> ColorResponse:
    check_existing_entity(db, Color, color.name, "Color")
    db_color = Color(**color.dict())
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    logger.info(f"Color created: {color.name}")
    return ColorResponse.from_orm(db_color)

def get_colors(db: Session) -> List[ColorResponse]:
    return [ColorResponse.from_orm(color) for color in db.query(Color).all()]

def get_color(db: Session, color_id: int) -> ColorResponse:
    color = db.query(Color).filter(Color.id == color_id).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return ColorResponse.from_orm(color)


# =======================
# Model Controller
# =======================
def create_model(db: Session, model: ModelCreate) -> ModelResponse:
    check_existing_entity(db, Model, model.name, "Model")
    db_model = Model(**model.dict())  # Consistent with the model name
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    logger.info(f"Model created: {model.name}")
    return ModelResponse.from_orm(db_model)

def get_models(db: Session) -> List[ModelResponse]:
    return [ModelResponse.from_orm(model) for model in db.query(Model).all()]

def get_model(db: Session, model_id: int) -> ModelResponse:
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return ModelResponse.from_orm(model)


# =======================
# Stock Status Controller
# =======================
def create_stock_status(db: Session, status: StockStatusCreate) -> StatusResponse:
    # Check for existing stock status with the same name
    existing_status = db.query(StockStatus).filter(StockStatus.name == status.name).first()
    if existing_status:
        raise HTTPException(status_code=400, detail="Stock status with this name already exists.")
    
    # Create a new StockStatus record
    db_status = StockStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    logger.info(f"Stock status created: {status.name}")
    
    # Return the newly created stock status response
    return StatusResponse.from_orm(db_status)

def get_stock_statuses(db: Session) -> list[StatusResponse]:
    return [StatusResponse.from_orm(status) for status in db.query(StockStatus).all()]

def get_stock_status(db: Session, status_id: int) -> StatusResponse:
    status = db.query(StockStatus).filter(StockStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Stock status not found")
    return StatusResponse.from_orm(status)



# =======================
# Supplier Controller
# =======================
def create_supplier(db: Session, supplier: SupplierCreate) -> SupplierResponse:
    # Check if the supplier with the same name exists (or by other unique identifiers)
    check_existing_entity(db, Supplier, supplier.name, "Supplier")
    
    # Extract contact info from the incoming request
    contact_info = supplier.contact_info

    # Create the supplier object excluding contact_info (as it's not directly part of the Supplier model)
    db_supplier = Supplier(
        name=supplier.name,
        email=contact_info.email if contact_info else None,  # Get email from contact_info
        phone=contact_info.phone if contact_info else None,  # Get phone from contact_info
        location=contact_info.location if contact_info else None,  # Get location from contact_info
        status=supplier.status
    )

    # Add the supplier to the session and commit it to the database
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    logger.info(f"Supplier created: {db_supplier.name}")
    
    # Return the SupplierResponse, including contact_info
    return SupplierResponse(
        id=db_supplier.id,
        name=db_supplier.name,
        contact_info=ContactInfo(
            email=db_supplier.email,
            phone=db_supplier.phone,
            location=db_supplier.location
        ),
        status=db_supplier.status,
        created_at=db_supplier.created_at
    )


def get_supplier(db: Session, supplier_id: int) -> SupplierResponse:
    # Fetch the supplier by ID
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Construct the response with contact_info
    contact_info = ContactInfo(
        email=supplier.email,
        phone=supplier.phone,
        location=supplier.location,
    )

    # Return the SupplierResponse
    return SupplierResponse(
        id=supplier.id,
        name=supplier.name,
        contact_info=contact_info,
        status=supplier.status,
        created_at=supplier.created_at
    )


def get_suppliers(db: Session) -> list[SupplierResponse]:
    # Fetch all suppliers
    suppliers = db.query(Supplier).all()

    # Map them into SupplierResponse objects
    return [
        SupplierResponse(
            id=supplier.id,
            name=supplier.name,
            contact_info=ContactInfo(
                email=supplier.email,
                phone=supplier.phone,
                location=supplier.location,
            ),
            status=supplier.status,
            created_at=supplier.created_at
        )
        for supplier in suppliers
    ]



# =======================
# Unit Controller
# =======================
def create_unit(db: Session, unit: UnitCreate) -> UnitResponse:
    check_existing_entity(db, Unit, unit.name, "Unit")
    db_unit = Unit(**unit.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    logger.info(f"Unit created: {unit.name}")
    return UnitResponse.from_orm(db_unit)

def get_units(db: Session) -> List[UnitResponse]:
    return [UnitResponse.from_orm(unit) for unit in db.query(Unit).all()]

def get_unit(db: Session, unit_id: int) -> UnitResponse:
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return UnitResponse.from_orm(unit)


# =======================
# Role Controller
# =======================
def create_role(role_data: RoleCreateRequest, db: Session):
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(
        name=role_data.name,
        description=role_data.description,
        created_at=datetime.utcnow()
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    logger.info(f"New role created: {role_data.name}")

    return RoleResponse(
        id=new_role.id,
        name=new_role.name,
        description=new_role.description,
        created_at=new_role.created_at
    )

def get_all_roles(db: Session):
    roles = db.query(Role).all()
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")
    return roles

def get_role_by_id(role_id: int, db: Session):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# =======================
# Gender Controller
# =======================
def create_gender(gender_data: GenderCreateRequest, db: Session):
    existing_gender = db.query(Gender).filter(Gender.name == gender_data.name).first()
    if existing_gender:
        raise HTTPException(status_code=400, detail="Gender already exists")

    new_gender = Gender(name=gender_data.name)
    db.add(new_gender)
    db.commit()
    db.refresh(new_gender)
    return GenderResponse(id=new_gender.id, name=new_gender.name)

def get_all_genders(db: Session):
    genders = db.query(Gender).all()
    if not genders:
        raise HTTPException(status_code=404, detail="No genders found")
    return genders


# =======================
# Utility Functions
# =======================
def check_existing_entity(db: Session, model, name: str, entity_name: str):
    if db.query(model).filter(model.name == name).first():
        raise HTTPException(status_code=400, detail=f"{entity_name} already exists")


# Controller for creating a new role
def create_role(role_data: RoleCreateRequest, db: Session):
    # Check if the role already exists
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    # Create the new role
    new_role = Role(
        name=role_data.name,
        description=role_data.description,
        created_at=datetime.utcnow()
    )

    # Add to the database and commit
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    logger.info(f"New role created: {role_data.name}")

    # Return the response model
    return RoleResponse(
        id=new_role.id,
        name=new_role.name,
        description=new_role.description,
        created_at=new_role.created_at
    )

# Get all roles
def get_all_roles(db: Session):
    roles = db.query(Role).all()  # Retrieve all roles from the database
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")
    return roles

# Get a single role by ID
def get_role_by_id(role_id: int, db: Session):
    role = db.query(Role).filter(Role.id == role_id).first()  # Retrieve the role by ID
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Controller for creating a new gender
def create_gender(gender_data: GenderCreateRequest, db: Session):
    # Check if the gender already exists
    existing_gender = db.query(Gender).filter(Gender.name == gender_data.name).first()
    if existing_gender:
        raise HTTPException(status_code=400, detail="Gender already exists")

    # Create the new gender
    new_gender = Gender(
        name=gender_data.name,
        description=gender_data.description,
        created_at=datetime.utcnow()
    )

    # Add to the database and commit
    db.add(new_gender)
    db.commit()
    db.refresh(new_gender)

    logger.info(f"New gender created: {gender_data.name}")

    # Return the response model
    return GenderResponse(
        id=new_gender.id,
        name=new_gender.name,
        description=new_gender.description,
        created_at=new_gender.created_at
    )

# Get all genders
def get_all_genders(db: Session):
    genders = db.query(Gender).all()  # Retrieve all genders from the database
    if not genders:
        raise HTTPException(status_code=404, detail="No genders found")
    return genders

# Get a single gender by ID
def get_gender_by_id(gender_id: int, db: Session):
    gender = db.query(Gender).filter(Gender.id == gender_id).first()  # Retrieve gender by ID
    if not gender:
        raise HTTPException(status_code=404, detail="Gender not found")
    return gender