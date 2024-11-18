from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.db.config import get_db, init_db, engine
from app.api.auth.routes import auth as auth_router
from app.api.utility.routes import utility as utility_router 
from app.api.inventory.routes import stock as stock_router
from app.api.products.routes import products as products_router
from sqlalchemy.orm import Session
from app.middlewares.services import add_cors
import logging

from app.utility.utc import get_current_cambodia_time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the FastAPI app
app = FastAPI(
    title="Demo API",
    version="1.0.0",
    description="API for authentication, inventory, products, and utility management",
)

# CORS middleware
add_cors(app)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


from app.api.SMTP.routes import SMTP as smtp_router

app.include_router(smtp_router, prefix="/api/smtp", tags=["SMTP"])

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(utility_router, prefix="/api/utility", tags=["Utility"])
app.include_router(stock_router, prefix="/api/stock", tags=["Stock"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])


@app.get("/current_time")
def get_current_time():
    # Use the utility to get current Cambodia time
    return {"current_time_in_cambodia": get_current_cambodia_time().strftime("%Y-%m-%d %H:%M:%S")}

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Health", "Check more url": "/health"}

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    client = TestClient(app)  # Initialize TestClient for making internal API requests
    current_timestamp = datetime.utcnow().isoformat()  # Get current timestamp in ISO format

    try:
        # Database connectivity check
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            db_status = "healthy" if result.scalar() == 1 else "unhealthy"
            db_message = "Database connection is successful" if db_status == "healthy" else "Database connection failed"
        
        # API Routers status check (check each router's availability)
        api_routers_status = "healthy"
        api_routers_message = "API routers are loaded and functional"
        
        # Check Stock API
        stock_check = {"status": "healthy", "message": "Stock API is responding correctly"}
        stock_response = client.get("/api/stock/stocks")  # Ensure this route exists and is functional
        if stock_response.status_code != 200:
            stock_check = {"status": "unhealthy", "message": f"Stock API is not responding as expected. Status Code: {stock_response.status_code}"}
            logging.error(f"Stock API failed with status code: {stock_response.status_code} - Response: {stock_response.text}")
        
        # Check Product API
        product_check = {"status": "healthy", "message": "Product API is responding correctly"}
        product_response = client.get("/api/products/products")  # Ensure the route is correct
        if product_response.status_code != 200:
            product_check = {"status": "unhealthy", "message": f"Product API is not responding as expected. Status Code: {product_response.status_code}"}
            logging.error(f"Product API failed with status code: {product_response.status_code} - Response: {product_response.text}")
        
        # Check Auth API
        auth_check = {"status": "healthy", "message": "Authentication API is working as expected"}
        # If needed, provide a token in the header
        # auth_token = "your-valid-jwt-token"  # Mock or retrieve a valid token
        # headers = {"Authorization": f"Bearer {auth_token}"}
        auth_response = client.get("/api/auth/users")  # Ensure the correct route is checked
        if auth_response.status_code != 200:
            auth_check = {"status": "unhealthy", "message": f"Authentication API is not responding as expected. Status Code: {auth_response.status_code}"}
            logging.error(f"Auth API failed with status code: {auth_response.status_code} - Response: {auth_response.text}")

        # Combine status for overall response
        overall_status = "healthy" if db_status == "healthy" and stock_check["status"] == "healthy" and product_check["status"] == "healthy" and auth_check["status"] == "healthy" else "unhealthy"

        # Build the response with more detailed info
        return {
            "status": overall_status,
            "message": "All systems are operational" if overall_status == "healthy" else "Some components are experiencing issues",
            "timestamp": current_timestamp,
            "components": {
                "database": {
                    "status": db_status,
                    "message": db_message,
                    "timestamp": current_timestamp
                },
                "api_routers": {
                    "status": api_routers_status,
                    "message": api_routers_message,
                    "timestamp": current_timestamp
                },
                "stock_check": stock_check,
                "product_check": product_check,
                "auth_check": auth_check,
            }
        }

    except Exception as e:
        # Log the error if any
        logging.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e), "timestamp": current_timestamp}
