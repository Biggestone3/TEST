from datetime import UTC, datetime
from uuid import uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from lna_db.core.types import Language, UUIDstr


class TimeStampedModel(Document):
    """Base model with created and updated timestamps."""

    id: UUIDstr = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        use_state_management = True

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(UTC)
        return await super().save(*args, **kwargs)


class UserPreferences(Document):
    """User preferences model."""

    source_ids: list[UUIDstr] = Field(
        default_factory=list, description="List of Source IDs that the user follows."
    )
    language: Language = Field(
        Language.UNKNOWN, description="Preferred language for reading news."
    )


class User(TimeStampedModel):
    """User model for the application."""

    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    full_name: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)

    class Settings:
        name = "users"


class Source(TimeStampedModel):
    """News source model."""

    name: str = Field(..., description="Display name of the source")
    url: str = Field(..., description="URL associated with this source")

    class Settings:
        name = "sources"


class Article(TimeStampedModel):
    """Article model representing a news article."""

    source_id: UUIDstr = Field(
        ..., description="Reference to the Source this article belongs to"
    )
    url: Indexed(str, unique=True)
    publish_date: datetime
    title: str
    content: str
    summary: str = ""
    language: Language = Language.UNKNOWN

    class Settings:
        name = "articles"


class AggregatedStory(TimeStampedModel):
    """Model representing a clustered or aggregated news story."""

    title: str
    summary: str
    language: Language
    publish_date: datetime
    article_ids: list[UUIDstr] = Field(default_factory=list)

    class Settings:
        name = "stories"
