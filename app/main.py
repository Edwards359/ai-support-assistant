from fastapi import FastAPI

from app.config import settings
from app import routes

app = FastAPI(title=settings.app_name)

app.include_router(routes.router)

# Run with: uvicorn app.main:app --reload
