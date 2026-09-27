from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables when application starts.
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "FitBuddy - AI Fitness Plan Generator "
        "using FastAPI, SQLite and Gemini"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(router)
