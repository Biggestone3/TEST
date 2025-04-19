import os
from contextlib import asynccontextmanager
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lna_db.db.mock_db import init_mock_db
from lna_db.db.mongo import init_database

from lna_app.api import auth, news, users


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyre-ignore
    """Lifespan context manager for FastAPI application.

    Handles startup and shutdown events:
    - Startup: Initialize database and Beanie ODM
    - Shutdown: Any cleanup if needed
    """
    # Startup
    load_dotenv()
    use_mock_db = os.environ.get("USE_MOCK_DB", "false").lower() == "true"
    username = str(os.environ.get("username_of_db"))
    password = str(os.environ.get("password_of_db"))
    mongo_uri_part2 = str(os.environ.get("mongo_uri_part2"))
    if use_mock_db:
        await init_mock_db()
    else:
        await init_database(
            username=username,
            password=password,
            mongo_uri_part2=mongo_uri_part2,
        )
    yield
    # Shutdown (if we need cleanup later)


app = FastAPI(
    title="LNA API",
    lifespan=lifespan,
)
# CORS Configuration
app.add_middleware(
    CORSMiddleware,  # pyre-ignore
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(news.router, prefix="/api/news")
app.include_router(users.router, prefix="/api/users")


@app.get("/")
async def root() -> dict[str, Union[str, dict[str, str]]]:
    return {
        "message": "LNA API is running",
        "endpoints": {"news": "/api/news", "auth": "/api/auth", "users": "/api/users"},
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
