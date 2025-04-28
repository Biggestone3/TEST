from datetime import UTC, datetime, timedelta
from uuid import UUID

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase

from lna_db.core.types import Language
from lna_db.models.news import AggregatedStory, Article, Source

# Create an in-memory MongoDB client for testing
client: AsyncMongoMockClient = AsyncMongoMockClient()
db: AsyncMongoMockDatabase = client.get_database("test_database")

# UUIDs
source_id: UUID = UUID("550e8400-e29b-41d4-a716-446655440000")
arabic_source_id: UUID = UUID("660e8400-e29b-41d4-a716-446655440000")
extra_source_id = UUID("770e8400-e29b-41d4-a716-446655440000")
extra_arabic_source_id = UUID("880e8400-e29b-41d4-a716-446655440000")

article_1_id: UUID = UUID("a631c8c8-5943-4d7d-b7bc-6d7f8e569e6b")
article_2_id: UUID = UUID("b724d849-5ad3-4e42-a29c-50049c6f4b38")
arabic_article_1_id: UUID = UUID("d631c8c8-5943-4d7d-b7bc-6d7f8e569e6b")
arabic_article_2_id: UUID = UUID("e724d849-5ad3-4e42-a29c-50049c6f4b38")
extra_article_en_id = UUID("f824d849-5ad3-4e42-a29c-50049c6f4b38")
extra_article_ar_id = UUID("b924d849-5ad3-4e42-a29c-50049c6f4b38")

new_source_id_1 = UUID("990e8400-e29b-41d4-a716-446655440000")
new_source_id_2 = UUID("aa0e8400-e29b-41d4-a716-446655440000")
new_source_id_3 = UUID("bb0e8400-e29b-41d4-a716-446655440000")

new_article_1_id = UUID("c824d849-5ad3-4e42-a29c-50049c6f4b38")
new_article_2_id = UUID("d824d849-5ad3-4e42-a29c-50049c6f4b38")
new_article_3_id = UUID("e824d849-5ad3-4e42-a29c-50049c6f4b38")


def get_mock_data() -> tuple[list[Source], list[Article], list[AggregatedStory]]:
    mock_sources = [
        Source(uuid=source_id, name="Global News Network", url="https://news.com"),
        Source(
            uuid=arabic_source_id,
            name="الشبكة الإخبارية العربية",
            url="https://arabnews.com",
        ),
        Source(
            uuid=extra_source_id, name="Daily Bulletin", url="https://dailybulletin.com"
        ),
        Source(
            uuid=extra_arabic_source_id, name="صحيفة اليوم", url="https://alyaum.com"
        ),
        Source(uuid=new_source_id_1, name="Tech Review", url="https://techreview.com"),
        Source(
            uuid=new_source_id_2, name="Middle East Times", url="https://metimes.com"
        ),
        Source(uuid=new_source_id_3, name="World Watch", url="https://worldwatch.com"),
    ]

    mock_articles = [
        Article(
            uuid=article_1_id,
            source_id=source_id,
            title="Breaking News",
            content="Something big happened! Here's the full story...",
            url="https://news.com/breaking",
            publish_date=datetime(2024, 3, 15, 12, 30, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            uuid=article_2_id,
            source_id=source_id,
            title="Technology Update",
            content="New advancements in AI and technology...",
            url="https://news.com/tech",
            publish_date=datetime(2024, 3, 15, 13, 0, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            uuid=extra_article_en_id,
            source_id=extra_source_id,
            title="More AI News",
            content="Another perspective on AI",
            url="https://dailybulletin.com/ai",
            publish_date=datetime(2024, 3, 15, 13, 30, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            uuid=arabic_article_1_id,
            source_id=arabic_source_id,
            title="تطورات التكنولوجيا",
            content="آخر التطورات في مجال الذكاء الاصطناعي...",
            url="https://arabnews.com/tech",
            publish_date=datetime(2024, 3, 15, 13, 30, tzinfo=UTC),
            language=Language.ARABIC,
        ),
        Article(
            uuid=arabic_article_2_id,
            source_id=arabic_source_id,
            title="مستقبل التقنية",
            content="توقعات مستقبل التكنولوجيا...",
            url="https://arabnews.com/future",
            publish_date=datetime(2024, 3, 15, 14, 0, tzinfo=UTC),
            language=Language.ARABIC,
        ),
        Article(
            uuid=extra_article_ar_id,
            source_id=extra_arabic_source_id,
            title="تقرير خاص عن الذكاء الاصطناعي",
            content="وجهة نظر جديدة حول الذكاء الاصطناعي",
            url="https://alyaum.com/ai",
            publish_date=datetime(2024, 3, 15, 14, 30, tzinfo=UTC),
            language=Language.ARABIC,
        ),
        Article(
            uuid=new_article_1_id,
            source_id=new_source_id_1,
            title="Quantum Computing Breakthrough",
            content="Scientists achieved a new milestone in quantum computing...",
            url="https://techreview.com/quantum",
            publish_date=datetime(2024, 3, 15, 15, 0, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
        Article(
            uuid=new_article_2_id,
            source_id=new_source_id_2,
            title="أخبار اقتصادية",
            content="تقرير عن الاقتصاد في الشرق الأوسط...",
            url="https://metimes.com/economy",
            publish_date=datetime(2024, 3, 15, 15, 30, tzinfo=UTC),
            language=Language.ARABIC,
        ),
        Article(
            uuid=new_article_3_id,
            source_id=new_source_id_3,
            title="Climate Change Update",
            content="A new UN report highlights climate progress and challenges...",
            url="https://worldwatch.com/climate",
            publish_date=datetime(2024, 3, 15, 16, 0, tzinfo=UTC),
            language=Language.ENGLISH,
        ),
    ]

    mock_stories = [
        AggregatedStory(
            uuid=UUID("c734d941-4fd2-4819-a3b7-7cc8971ab25e"),
            title="Technology and AI Developments",
            summary="Latest developments and predictions in technology and AI",
            language=Language.ENGLISH,
            publish_date=datetime(2024, 3, 15, 12, 30, tzinfo=UTC),
            article_ids=[
                article_1_id,
                article_2_id,
                extra_article_en_id,
                new_article_1_id,
                new_article_3_id,
            ],
            aggregation_key="",
            aggregator="manual_create",
        ),
        AggregatedStory(
            aggregation_key="",
            aggregator="manual_create",
            uuid=UUID("d834d941-4fd2-4819-a3b7-7cc8971ab25e"),
            title="مستقبل التكنولوجيا والذكاء الاصطناعي",
            summary="آخر التطورات والتوقعات في مجال التكنولوجيا والذكاء الاصطناعي",
            language=Language.ARABIC,
            publish_date=datetime(2024, 3, 15, 13, 30, tzinfo=UTC),
            article_ids=[
                arabic_article_1_id,
                arabic_article_2_id,
                extra_article_ar_id,
                new_article_2_id,
            ],
        ),
    ]

    # Add 30 auto-generated stories

    base_time = datetime(2024, 3, 16, 8, 0, tzinfo=UTC)

    for i in range(50):
        story_id = UUID(f"11111111-1111-1111-1111-{str(i).zfill(12)}")
        publish_date = base_time + timedelta(minutes=i)
        mock_stories.append(
            AggregatedStory(
                uuid=story_id,
                title=f"Generated Story {i + 1}",
                summary=f"Auto-generated summary for story {i + 1}",
                language=Language.ENGLISH if i % 2 == 0 else Language.ARABIC,
                publish_date=publish_date,
                article_ids=[
                    new_article_1_id,
                    new_article_2_id if i % 2 == 0 else new_article_3_id,
                ],
                aggregator="mock_db",
                aggregation_key=f"mock_key_{i}",
            )
        )

    return mock_sources, mock_articles, mock_stories


async def init_mock_db() -> None:
    """Initialize the mock database with sample data."""
    await init_beanie(
        database=db,  # type: ignore
        document_models=[Source, Article, AggregatedStory],
    )

    await Source.delete_all()
    await Article.delete_all()
    await AggregatedStory.delete_all()

    mock_sources, mock_articles, mock_stories = get_mock_data()

    for source in mock_sources:
        await source.save()

    for article in mock_articles:
        await article.save()

    for story in mock_stories:
        await story.save()
