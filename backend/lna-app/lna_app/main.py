import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from lna_db.db.session import init_database

from lna_app.api import news


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.

    Handles startup and shutdown events:
    - Startup: Initialize database and Beanie ODM
    - Shutdown: Any cleanup if needed
    """
    # Startup
    load_dotenv()
    use_mock_db = os.environ.get("USE_MOCK_DB", "false").lower() == "true"
    await init_database(use_mock_db)
    yield
    # Shutdown (if we need cleanup later)


app = FastAPI(
    title="LNA API",
    lifespan=lifespan,
)

app.include_router(news.router, prefix="/news")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
