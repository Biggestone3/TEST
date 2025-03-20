import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from lna_db.db.mock_db import init_mock_db
from lna_db.db.mongo import init_database
from lna_app.api import news


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
    if use_mock_db:
        await init_mock_db()
    else:
        await init_database()
    yield
    # Shutdown (if we need cleanup later)


app = FastAPI(
    title="LNA API",
    lifespan=lifespan,
)

app.include_router(news.router, prefix="/api/news")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
