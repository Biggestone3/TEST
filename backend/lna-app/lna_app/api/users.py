from typing import Optional

from fastapi import APIRouter, Depends
from lna_db.core.types import Language, UUIDstr
from lna_db.models.news import User

from lna_app.auth_utils import get_current_user, get_current_user_optional

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user_details(
    user: Optional[User] = Depends(get_current_user_optional),
) -> Optional[User]:
    return user


@router.post("/update-preferences")
async def update_user_preferences(
    language: str,
    source_ids: Optional[list[UUIDstr]] = None,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    if language:
        try:
            current_user.preferences.language = Language(language)
        except ValueError:
            current_user.preferences.language = Language("en")

    if source_ids:
        current_user.preferences.source_ids = source_ids

    await current_user.save()  # type: ignore[attr-defined]
    return {
        "message": "User preferences updated successfully",
        "user_id": str(current_user.id),
    }
