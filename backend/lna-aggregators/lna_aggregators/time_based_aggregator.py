import logging
from datetime import datetime, timedelta, timezone

from beanie.operators import In
from lna_db.core.types import Language, UUIDstr
from lna_db.db.mongo import init_database
from lna_db.models.news import AggregatedStory, Article

from lna_aggregators.aggregator import AbstractAggregator
from lna_aggregators.summarizer import Summarizer


class TimeBasedAggregator(AbstractAggregator):
    """
    will aggregate articles into stories based on time.
    All articles belonging to the same hour will be in the same story.
    """

    def __init__(
        self, database_username: str, database_password: str, mongo_uri_part2: str
    ) -> None:
        self.aggregator = TimeBasedAggregator.__name__
        self.database_username = database_username
        self.database_password = database_password
        self.mongo_uri_part2 = mongo_uri_part2

    async def aggregate_stories(self, start_time: datetime, end_time: datetime) -> None:
        # prepare db
        await init_database(
            username=self.database_username,
            password=self.database_password,
            mongo_uri_part2=self.mongo_uri_part2,
        )

        logging.info(
            f"started aggregating stories by time, between {start_time} and {end_time}"
        )

        articles_in_range = await Article.find(
            Article.publish_date >= start_time, Article.publish_date <= end_time
        ).to_list()

        article_id_to_article = {article.uuid: article for article in articles_in_range}

        logging.info(f"found {len(articles_in_range)} articles in range")

        summarizer = Summarizer()

        # for each article find the key which it is associated with
        agg_keys_to_articles_to_add: dict[str, list[UUIDstr]] = {}
        for article in articles_in_range:
            key = self._get_aggregation_key(article.publish_date)
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
                    source_ids=[],
                    aggregation_key=key,
                ),
            )

            # add the article ids with no repetition
            story.article_ids.extend(article_ids)
            story.article_ids = list(set(story.article_ids))

            # add source ids with no repetition
            story.source_ids.extend(
                [
                    article_id_to_article[article_id].source_id
                    for article_id in article_ids
                ]
            )
            story.source_ids = list(set(story.source_ids))

            # generate summary
            previous_summary = story.summary
            new_articles_content = ""
            for article_id in article_ids:
                article = article_id_to_article[article_id]
                title = article.title
                content = article.content
                new_articles_content += f"[title]\n{title}\n\n[content]\n{content}\n"

            story.summary = await summarizer.generate_summary(
                previous_summary=previous_summary,
                new_articles_content=new_articles_content,
            )

            story.title = await summarizer.generate_title(summary=story.summary)

            # save (beanie does not support bulk upsert)
            await story.save()

    def _get_aggregation_key(self, time: datetime) -> str:
        return self._get_aggregation_key_and_next_hour(time)[0]

    def _get_aggregation_key_and_next_hour(
        self, time: datetime
    ) -> tuple[str, datetime]:
        current_hour = time.replace(minute=0, second=0, microsecond=0)
        next_hour = current_hour + timedelta(hours=1)
        return (f"{current_hour}_{next_hour}", next_hour)
