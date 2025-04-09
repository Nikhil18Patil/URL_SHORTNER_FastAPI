from fastapi import FastAPI
from app.database import Base, engine
from app.routers import url

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clean URL Shortener")

# Include the URL shortener routes
app.include_router(url.router)


@app.get("/")
def read_root():
    return {
        "message": "👋 Hey there! Welcome to the Clean URL Shortener API.",
        f"usage": "Use {http://127.0.0.1:8000/docs} for Swagger UI or {http://127.0.0.1:8000/redoc} for ReDoc to explore and test the API."
    }
