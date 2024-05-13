from daemons.base import BaseDaemon
from models.source import Source
from routers.observer import update_subscribers
from daemons.utils import add_data_to_db


class FakeAggDaemon(BaseDaemon):
    def __init__(self, delay: int) -> None:
        super().__init__(self.task, delay)

    async def task(self) -> None:
        print("Fake Aggregator Daemon task started")

        source = Source(
            title="fake title",
            link="fake link",
            media="fake media",
            author="fake author",
            date="fake date",
        )

        if (source_id := add_data_to_db(source)) != -1:
            update_subscribers(source_id)

        print("Fake Aggregator Daemon task finished")
