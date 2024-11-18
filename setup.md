To start building your FastAPI project with the folder structure you provided, the first step is to set up the necessary packages and tools. Since you’re using SQLite for local development and plan to use PostgreSQL for production, I'll guide you through installing the required dependencies and setting up the environment.

### Step 1: Set up the environment and install dependencies

First, create a virtual environment to isolate your project dependencies.

#### 1.1 Create a virtual environment

```bash
python3 -m venv venv
```

#### 1.2 Activate the virtual environment

- **For macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **For Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

#### 1.3 Install the necessary dependencies

Run the following to install FastAPI, Uvicorn (for running the development server), SQLAlchemy (for database interaction), and other important packages:

```bash
pip install fastapi uvicorn python-dotenv sqlalchemy alembic psycopg2-binary passlib bcrypt python-jose[cryptography] pydantic
```

### Step 2: Create `requirements.txt`

Once you've installed the necessary dependencies, you can generate a `requirements.txt` file to keep track of the installed packages.

```bash
pip freeze > requirements.txt
```

### Step 3: Initialize SQLite Database for Local Development

Since you plan to use SQLite for local development, you can set up the database in your `.env` file.

#### 3.1 Create a `.env` file in the root of your project:

```bash
touch .env
```

Inside the `.env` file, define the following:

```bash
DATABASE_URL=sqlite:///./app/db/database.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Later, when moving to production with PostgreSQL, you will update the `DATABASE_URL` to match your PostgreSQL connection string.

### Step 4: Configure Database Settings

You’ve already structured your `db` folder. Ensure your `config.py` in `app/db` looks like this to support SQLite for local development and PostgreSQL for production:

```python
# app/db/config.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the DATABASE_URL from the environment, defaulting to SQLite for local testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app/db/database.db")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create a SessionLocal class for creating session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 5: Set up Alembic for Migrations

For managing migrations, especially when moving to PostgreSQL, Alembic is necessary. Install Alembic:

```bash
pip install alembic
```

Then, initialize Alembic:

```bash
alembic init alembic
```

Configure the Alembic `env.py` to use your database setup, pointing to the `DATABASE_URL` from the `.env` file.

### Step 6: Create `main.py`

Here’s a simple `main.py` setup to bootstrap the FastAPI application:

```python
# main.py

from fastapi import FastAPI
from app.db.config import init_db
from app.api.auth import auth_router
from app.api.inventory import inventory_router
from app.api.products import products_router
from app.api.utility import utility_router

app = FastAPI(
    title="Demo API",
    version="1.0.0",
    description="API for authentication, inventory, products, and utility management",
)

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()

# Include the routers
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
app.include_router(utility_router, prefix="/api/utility", tags=["Utility"])

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Demo API"}
```

### Step 7: Run the Development Server

To run the FastAPI server locally:

```bash
uvicorn main:app --reload
```

This will run the API at `http://127.0.0.1:8000`.

---

### What's Next

Once this basic setup is working, you can start building out the `auth`, `inventory`, `products`, and `utility` modules. These will include the FastAPI routes, schemas (using Pydantic), and database models (using SQLAlchemy).

Let me know when you're ready to move forward with implementing the modules or need help with specific aspects like authentication, route creation, or other utilities.
