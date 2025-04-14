from abc import ABC
from datetime import datetime


class AbstractAggregator(ABC):
    async def aggregate_stories(start_time: datetime, end_time: datetime) -> None:
        pass
