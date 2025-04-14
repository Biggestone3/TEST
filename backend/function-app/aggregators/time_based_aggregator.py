import logging
from datetime import datetime, timedelta, timezone

from beanie.operators import In
from lna_db.core.types import Language, UUIDstr
from lna_db.models.news import AggregatedStory, Article

from aggregators.aggregator import AbstractAggregator


class TimeBasedAggregator(AbstractAggregator):
    """
    will aggregate articles into stories based on time.
    All articles belonging to the same hour will be in the same story.
    """

    def __init__(self) -> None:
        self.aggregator = TimeBasedAggregator.__name__

    async def aggregate_stories(self, start_time: datetime, end_time: datetime) -> None:
        logging.info(
            f"started aggregating stories by time, between {start_time} and {end_time}"
        )

        articles_in_range = await Article.find(
            Article.publish_date >= start_time, Article.publish_date <= end_time
        ).to_list()

        logging.info(f"found {len(articles_in_range)} articles in range")

        # for each article find the key which it is associated with
        agg_keys_to_articles_to_add: dict[str, list[UUIDstr]] = {}
        for article in articles_in_range:
            key = self.get_aggregation_key(article.publish_date)
            agg_keys_to_articles_to_add.setdefault(key, []).append(article.uuid)

        # get stories with the corresponding aggregation keys
        existing_stories = await AggregatedStory.find(
            AggregatedStory.aggregator == self.aggregator,
            In(AggregatedStory.aggregation_key, agg_keys_to_articles_to_add.keys()),
        ).to_list()

        agg_keys_to_stories = {
            story.aggregation_key: story for story in existing_stories
        }

        for key, article_ids in agg_keys_to_articles_to_add.items():
            # get the corresponding story
            story = agg_keys_to_stories.setdefault(
                key,
                AggregatedStory(
                    title=f"news for range {key}",
                    summary=f"placeholder summary for range {key}",
                    language=Language.UNKNOWN,
                    publish_date=datetime.now(timezone.utc),
                    aggregator=self.aggregator,
                    article_ids=[],
                    aggregation_key=key,
                ),
            )

            # add the article ids with no repetition
            old_article_ids = story.article_ids
            old_article_ids.extend(article_ids)
            story.article_ids = set(old_article_ids)

            # save (beanie does not support bulk upsert)
            await story.save()

    def get_aggregation_key(self, time: datetime) -> str:
        return self.get_aggregation_key_and_next_hour(time)[0]

    def get_aggregation_key_and_next_hour(self, time: datetime) -> tuple[str, datetime]:
        current_hour = time.replace(minute=0, second=0, microsecond=0)
        next_hour = current_hour + timedelta(hours=1)
        return (f"{current_hour}_{next_hour}", next_hour)
