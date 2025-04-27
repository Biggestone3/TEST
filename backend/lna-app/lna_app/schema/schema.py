from datetime import datetime, timezone
from typing import Annotated, Any, Optional
from uuid import uuid4

from beanie import Indexed
from lna_db.core.types import Language, UUIDstr
from pydantic import BaseModel, EmailStr, Field

# --- Existing Schemas ---


class UserPreferences(BaseModel):
    """
    Stores the user's preferences, such as which sources they follow
    and their preferred language.
    Attributes:
        source_ids: List of unique identifiers (UUIDs) of the sources a user follows.
        language: The preferred language in which the user wants to read news.
    """

    source_ids: list[UUIDstr] = Field(
        default_factory=list, description="List of Source IDs that the user follows."
    )
    language: Language = Field(
        default=Language.UNKNOWN, description="Preferred language for reading news."
    )


class User(BaseModel):
    """
    Represents a user in the system.
    Attributes:
        id: Unique identifier for the user.
        email: Email address used for contact and authentication.
        preferences: User preferences, including source subscriptions and language.
    """

    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the article (UUID)."
    )
    email: EmailStr = Field(..., description="User's email address.")
    username: Annotated[str, Indexed(unique=True)] = Field(
        ..., description="Username of the user"
    )
    full_name: str = Field(..., description="Full name of the user")
    preferences: UserPreferences = Field(default_factory=lambda: UserPreferences())


class Source(BaseModel):
    """
    Represents a source from which articles can be collected.
    Attributes:
        id: Unique identifier for the source (UUID).
        name: Display name of the source.
        urls: List of URLs associated with the source (e.g., homepage, RSS feed).
    """

    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the article (UUID)."
    )
    name: str = Field(
        ..., description="Display name of the source (e.g., 'Daily Star Lebanon')."
    )
    url: str = Field(
        ..., description="URL (homepage or RSS feed) associated with this source."
    )


class Article(BaseModel):
    """
    Represents a single article fetched from a given source.
    Attributes:
        id: Unique identifier for the article (UUID).
        source_id: ID referencing the Source from which this article was collected.
        url: Direct URL to the article.
        publish_date: Date and time when the article was published.
        title: Title of the article.
        content: Full body text of the article.
        language: Language of the article, defaults to UNKNOWN if undetermined.
    """

    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the article (UUID)."
    )
    source_id: UUIDstr = Field(
        ..., description="Reference to the Source.id this article belongs to."
    )
    url: str = Field(..., description="Direct URL to the published article.")
    publish_date: datetime = Field(
        ..., description="Date and time when the article was published."
    )
    title: str = Field(..., description="Title of the article.")
    content: str = Field(..., description="Full body text of the article.")
    language: Language = Field(
        Language.UNKNOWN, description="Language of the article; defaults to UNKNOWN."
    )


class AggregatedStory(BaseModel):
    """
    Represents a clustered or aggregated news 'event' or 'story,'
    which groups multiple articles covering the same topic or event.
    Attributes:
        id: Unique identifier for the aggregated story (UUID).
        title: System-generated or AI-generated title describing the cluster.
        summary: A short summary of the story or event.
        language: Language of the aggregated story (usually the dominant language).
        publish_date: Representative date for the story (e.g.,
        earliest publish date among articles).
        article_ids: List of article IDs (UUIDs) that belong to this aggregated story.
    """

    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the article (UUID)."
    )
    title: str = Field(..., description="Descriptive title for the aggregated story.")
    summary: str = Field(
        ..., description="Short overview or summary of the aggregated story."
    )
    language: Language = Field(..., description="Language of the aggregated story.")
    publish_date: datetime = Field(
        ..., description="Representative publish date (e.g., earliest article date)."
    )
    article_ids: list[UUIDstr] = Field(
        ..., description="List of UUIDs referencing articles in this story cluster."
    )


class AggregatedStoryListResponse(BaseModel):
    stories: list[AggregatedStory] = Field(
        ..., description="List of aggregated stories."
    )


class UserListResponse(BaseModel):
    users: list[User] = Field(..., description="List of users.")


class SourceListResponse(BaseModel):
    sources: list[Source] = Field(..., description="List of news sources.")


class ArticleListResponse(BaseModel):
    articles: list[Article] = Field(..., description="List of articles.")


class UserCreate(BaseModel):
    google_id: str
    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the user (UUID)."
    )
    email: EmailStr
    username: str
    full_name: str
    preferences: dict[str, Any] = {}


class SourceCreate(BaseModel):
    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the source (UUID)."
    )
    name: str
    url: str


class ArticleCreate(BaseModel):
    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the article (UUID)."
    )
    source_id: UUIDstr
    url: str
    publish_date: datetime
    title: str
    content: str
    language: str


class AggregatedStoryCreate(BaseModel):
    uuid: UUIDstr = Field(
        default_factory=uuid4, description="Unique identifier for the story (UUID)."
    )
    title: str
    summary: str
    language: str
    publish_date: datetime
    article_ids: list[UUIDstr]


# --- New Request Model for Stories Filtering ---
class StoryFilterRequest(BaseModel):
    cuttof_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="this is the cutoff date. the api will return stories with "
        "publish date earlier than date.",
    )
    offset: int = Field(default=0, description="this is the offset for pagination")
    page_size: int = Field(
        default=0, description="this is the page_size for pagination"
    )
    source_ids: Optional[list[UUIDstr]] = Field(
        default_factory=list,
        description="We will return stories where all source ids are present",
    )


# --- New Enriched Response Models ---


class EnrichedArticle(BaseModel):
    """Represents article info for a story, including the source details."""

    id: UUIDstr
    source_name: str
    source_url: Optional[str] = None


class EnrichedStory(BaseModel):
    """Represents a story with its enriched article data."""

    id: UUIDstr
    title: str
    summary: str
    language: str
    publish_date: datetime
    articles: list[EnrichedArticle]
    imageUrl: Optional[str] = None


class EnrichedStoryListResponse(BaseModel):
    """
    Top-level response model to encapsulate the enriched stories list.
    """

    enriched_stories: list[EnrichedStory]
