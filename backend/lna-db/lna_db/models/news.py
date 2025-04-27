from datetime import UTC, datetime
from typing import Annotated, Any, Self
from uuid import uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from lna_db.core.types import Language, UUIDstr


class TimeStampedModel(Document):
    """Base model with created and updated timestamps."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the model was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the model was last updated",
    )

    class Settings:
        use_state_management = True

    async def save(self, *args: Any, **kwargs: Any) -> Self:
        self.updated_at = datetime.now(UTC)
        return await super().save(*args, **kwargs)


class UserPreferences(Document):
    """User preferences model."""

    source_ids: list[UUIDstr] = Field(
        default_factory=list, description="List of Source IDs that the user follows."
    )
    language: Language = Field(
        default=Language.UNKNOWN, description="Preferred language for reading news."
    )


class User(TimeStampedModel):
    """User model for the application."""

    uuid: UUIDstr = Field(default_factory=uuid4)
    google_id: Annotated[str, Indexed(unique=True)] = Field(...)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(
        ..., description="Email address of the user"
    )
    username: Annotated[str, Indexed(unique=True)] = Field(
        ..., description="Username of the user"
    )
    full_name: str = Field(..., description="Full name of the user")
    preferences: UserPreferences = Field(default_factory=lambda: UserPreferences())

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "users"


class Source(TimeStampedModel):
    """News source model."""

    uuid: UUIDstr = Field(default_factory=uuid4)
    name: str = Field(..., description="Display name of the source")
    url: str = Field(..., description="URL associated with this source")

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "sources"

    content_html_key: tuple[str, str] = Field(
        default=("", ""), description="The place to get info from the actual webpage."
    )
    has_rss: bool = Field(
        default=True,
        description="Boolean value that determines whether "
        "a webpage has an RSS value or not.",
    )


class Article(TimeStampedModel):
    """Article model representing a news article."""

    uuid: UUIDstr = Field(default_factory=uuid4)
    source_id: UUIDstr = Field(
        ..., description="Reference to the Source this article belongs to"
    )
    url: Annotated[str, Indexed(unique=True)] = Field(
        ..., description="URL of the article"
    )
    publish_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Publish date of the article",
    )
    title: str = Field(..., description="Title of the article")
    content: str = Field(..., description="Content of the article")

    language: Language = Language.UNKNOWN

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "articles"


class AggregatedStory(TimeStampedModel):
    """Model representing a clustered or aggregated news story."""

    uuid: UUIDstr = Field(default_factory=uuid4)
    title: str = Field(..., description="Title of the aggregated story")
    summary: str = Field(..., description="Summary of the aggregated story")
    language: Language = Field(..., description="Language of the aggregated story")
    publish_date: datetime = Field(
        ..., description="Publish date of the aggregated story"
    )
    article_ids: list[UUIDstr] = Field(default_factory=list)
    aggregator: str = Field(
        ..., description="The aggregator which lead to this aggregated story"
    )
    aggregation_key: str = Field(
        ...,
        description="The key of the aggregation, for time based it will be the hour, "
        "for topic based it will be the topic",
    )
    source_ids: list[UUIDstr] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "stories"
