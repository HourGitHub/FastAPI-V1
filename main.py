from fastapi import FastAPI
from app.db.config import init_db
from app.api.utility.routes import utility_router 
from app.api.auth.routes import auth_router 
# from app.api.product import routes as product_routes  # Assuming product routes are added
# from app.api.stock import routes as stock_routes  # Assuming stock routes are added

app = FastAPI(title="Demo API", version="1.0.0")

# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Include API routers for different modules
app.include_router(utility_router, prefix="/api/utility", tags=["Utility"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])  # Include auth routes
# app.include_router(product_routes.router, prefix="/api/product", tags=["Product"])  # Include product routes
# app.include_router(stock_routes.router, prefix="/api/stock", tags=["Stock"])  # Include stock routes

# Root route for basic health check
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FastAPI application"}

# Health check route to check if the API is running
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
