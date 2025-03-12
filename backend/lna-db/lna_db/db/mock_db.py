from datetime import UTC, datetime
from uuid import UUID

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase

from lna_db.core.types import Language
from lna_db.models.news import AggregatedStory, Article, Source

# Create an in-memory MongoDB client for testing
client: AsyncMongoMockClient = AsyncMongoMockClient()
db: AsyncMongoMockDatabase = client.get_database("test_database")

# Sample data with fixed UUIDs for testing
source_id: UUID = UUID("550e8400-e29b-41d4-a716-446655440000")
arabic_source_id: UUID = UUID("660e8400-e29b-41d4-a716-446655440000")

article_1_id: UUID = UUID("a631c8c8-5943-4d7d-b7bc-6d7f8e569e6b")
article_2_id: UUID = UUID("b724d849-5ad3-4e42-a29c-50049c6f4b38")
arabic_article_1_id: UUID = UUID("d631c8c8-5943-4d7d-b7bc-6d7f8e569e6b")
arabic_article_2_id: UUID = UUID("e724d849-5ad3-4e42-a29c-50049c6f4b38")


def get_mock_data() -> tuple[list[Source], list[Article], list[AggregatedStory]]:
    """Get the mock data for testing."""
    mock_sources = [
        Source(
            id=source_id,
            name="Global News Network",
            url="https://news.com",
        ),
        Source(
            id=arabic_source_id,
            name="الشبكة الإخبارية العربية",
            url="https://arabnews.com",
        ),
    ]

    mock_articles = [
        Article(
            id=article_1_id,
            source_id=source_id,
            title="Breaking News",
            content="Something big happened! Here's the full story...",
            summary="Something big happened!",
            url="https://news.com/breaking",
            publish_date=datetime(2024, 3, 15, 12, 30, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            id=article_2_id,
            source_id=source_id,
            title="Technology Update",
            content="New advancements in AI and technology...",
            summary="Latest tech developments",
            url="https://news.com/tech",
            publish_date=datetime(2024, 3, 15, 13, 0, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            id=arabic_article_1_id,
            source_id=arabic_source_id,
            title="تطورات التكنولوجيا",
            content="آخر التطورات في مجال الذكاء الاصطناعي...",
            summary="تقدم كبير في مجال الذكاء الاصطناعي",
            url="https://arabnews.com/tech",
            publish_date=datetime(2024, 3, 15, 13, 30, tzinfo=UTC),
            language=Language.ARABIC,
        ),
        Article(
            id=arabic_article_2_id,
            source_id=arabic_source_id,
            title="مستقبل التقنية",
            content="توقعات مستقبل التكنولوجيا...",
            summary="نظرة على مستقبل التقنية",
            url="https://arabnews.com/future",
            publish_date=datetime(2024, 3, 15, 14, 0, tzinfo=UTC),
            language=Language.ARABIC,
        ),
    ]

    mock_stories = [
        AggregatedStory(
            id=UUID("c734d941-4fd2-4819-a3b7-7cc8971ab25e"),
            title="Technology and AI Developments",
            summary="Latest developments and predictions in technology and AI",
            language=Language.ENGLISH,
            publish_date=datetime(2024, 3, 15, 12, 30, tzinfo=UTC),
            article_ids=[article_1_id, article_2_id],
        ),
        AggregatedStory(
            id=UUID("d834d941-4fd2-4819-a3b7-7cc8971ab25e"),
            title="مستقبل التكنولوجيا والذكاء الاصطناعي",
            summary="آخر التطورات والتوقعات في مجال التكنولوجيا والذكاء الاصطناعي",
            language=Language.ARABIC,
            publish_date=datetime(2024, 3, 15, 13, 30, tzinfo=UTC),
            article_ids=[arabic_article_1_id, arabic_article_2_id],
        ),
    ]

    return mock_sources, mock_articles, mock_stories


async def init_mock_db() -> None:
    """Initialize the mock database with sample data."""
    # Initialize Beanie with our models
    await init_beanie(
        database=db,  # type: ignore
        document_models=[Source, Article, AggregatedStory],
    )

    # Clear existing data
    await Source.delete_all()
    await Article.delete_all()
    await AggregatedStory.delete_all()

    # Get mock data
    mock_sources, mock_articles, mock_stories = get_mock_data()

    # Insert mock data
    for source in mock_sources:
        await source.save()

    for article in mock_articles:
        await article.save()

    for story in mock_stories:
        await story.save()
