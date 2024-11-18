# app/db/__init__.py

from .config import get_db
from .models.LoginLog import LoginLog  # Corrected import
from .models.user import User

# Importing other models as needed
from .models.utility import Brand, Category, Color, Gender, Model, Role, StockStatus, Supplier, Unit

# Add to __all__ to ensure these models are available when importing * from this file
__all__ = [
    "get_db", "LoginLog", "User", 
    "Brand", "Category", "Color", "Gender", "Model", "Role", 
    "StockStatus", "Supplier", "Unit"
]
