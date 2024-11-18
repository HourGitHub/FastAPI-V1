# app/api/__init__.py

from .auth.routes import auth_router
# from .product import product_router  # If you have product routes
# from .stock import stock_router  # If you have stock routes
from .utility.routes import utility_router  # If you have utility routes

__all__ = [
    "auth_router",
    # "product_router",  # Uncomment if you're using product routes
    # "stock_router",  # Uncomment if you're using stock routes
    "utility_router"  # Uncomment if you're using utility routes
]
