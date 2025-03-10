from lna_db.models.news import AggregatedStory as DbAggregatedStory

from lna_app.schema.schema import AggregatedStory


async def get_stories_paginated(
    skip: int = 0, limit: int = 10
) -> list[AggregatedStory]:
    db_stories = await DbAggregatedStory.find().skip(skip).limit(limit).to_list()
    return [AggregatedStory(**story.model_dump()) for story in db_stories]
