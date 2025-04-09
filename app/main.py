import logging
logging.basicConfig(level=logging.INFO)
print("🚀 App is starting...")

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import url
from mangum import Mangum

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clean URL Shortener")

app.include_router(url.router)

@app.get("/")
def read_root():
    return {
        "message": "👋 Hey there! Welcome to the Clean URL Shortener API.",
        "usage": "Visit /docs for Swagger UI or /redoc for ReDoc to explore and test the API."
    }

handler = Mangum(app)
