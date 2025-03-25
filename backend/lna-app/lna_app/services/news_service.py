from uuid import UUID
from lna_db.models.news import AggregatedStory as DbAggregatedStory, Article, Source

async def get_stories_enriched():
    db_stories = await DbAggregatedStory.find_all().to_list()
    enriched_stories = []

    for story in db_stories:
        # Convert to UUIDs just in case they're strings
        article_ids = [UUID(str(aid)) for aid in story.article_ids]

        articles = await Article.find({"_id": {"$in": article_ids}}).to_list()

        source_ids = list(set(article.source_id for article in articles))
        sources = await Source.find({"_id": {"$in": source_ids}}).to_list()
        source_map = {
            str(source.id): {
                "name": source.name,
                "url": source.url
            }
            for source in sources
        }

        enriched_articles = [
            {
                "id": str(article.id),
                "source_name": source_map.get(str(article.source_id), {}).get("name", "Unknown Source"),
                "source_url": source_map.get(str(article.source_id), {}).get("url", None),
            }
            for article in articles
        ]

        enriched_stories.append({
            "id": str(story.id),
            "title": story.title,
            "summary": story.summary,
            "language": story.language.value,
            "publish_date": story.publish_date.isoformat(),
            "articles": enriched_articles,
        })

    return {"stories": enriched_stories}
