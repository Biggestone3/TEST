from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, cast

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from lna_db.models.news import User
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Required Google fields
    GOOGLE_CLIENT_ID: str = "dev-client-id"
    GOOGLE_CLIENT_SECRET: str = "dev-client-secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/callback"

    # JWT Configuration
    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file: Path = Path(__file__).parent.parent / ".env"  # Absolute path
        env_file_encoding: str = "utf-8"
        extra: str = "ignore"


# Initialize settings without calling parent class __init__
settings = Settings()
print(f"[CONFIG] Client Secret Loaded: {settings.GOOGLE_CLIENT_SECRET is not None}")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/google/callback")


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_jwt_token(token)
        if not payload or "sub" not in payload:
            return None
        user_id = payload["sub"]
        # Using cast here to handle the PydanticObjectId correctly
        return await User.get(cast(PydanticObjectId, user_id))
    except Exception:
        return None


async def get_current_user(
    user: Optional[User] = Depends(get_current_user_optional),
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
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
