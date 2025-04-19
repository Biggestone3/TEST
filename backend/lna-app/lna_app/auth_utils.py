import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from lna_db.models.news import User
from pydantic_settings import BaseSettings

# Load environment variables before defining settings
load_dotenv()


class Settings(BaseSettings):
    # Required Google fields
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: Optional[str] = os.getenv("GOOGLE_REDIRECT_URI")

    # JWT Configuration
    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Frontend
    FRONTEND_URL: str | None = os.getenv("FRONTEND_URL")

    class Config:
        env_file: Path = Path(__file__).parent.parent / ".env"  # Absolute path
        env_file_encoding: str = "utf-8"
        extra: str = "ignore"


settings = Settings()
print(f"[CONFIG] Client Secret Loaded: {settings.GOOGLE_CLIENT_SECRET is not None}")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/google/callback")


async def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> User | None:
    if not token:
        return None
    try:
        payload = decode_jwt_token(token)
        if not payload or "sub" not in payload:
            return None
        user_id = payload["sub"]
        return await User.get(user_id)
    except Exception:
        return None


async def get_current_user(
    user: User | None = Depends(get_current_user_optional),
) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_jwt_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
