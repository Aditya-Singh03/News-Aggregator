from daemons.base import BaseDaemon
from routers.observer import update_subscribers
from daemons.utils import add_data_to_db
from scrapers.news_api import call_everything
from datetime import datetime, timedelta

PAGE_SIZE = 100
PLACEHOLDER_KEYWORD = "the"


def get_dt_week() -> tuple[str, str]:
    today = datetime.now()
    last_week = today - timedelta(days=7)
    return last_week.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


class NewsAPIAggDaemon(BaseDaemon):
    def __init__(self, delay: int) -> None:
        self.page_number = 1
        super().__init__(self.task, delay)

    async def task(self) -> None:
        print("NewsAPI Aggregator Daemon task started with page=", self.page_number)

        list_sources = call_everything(
            keywords=PLACEHOLDER_KEYWORD,
            pageSize=PAGE_SIZE,
            page=self.page_number,
        )

        list_source_ids = []

        if not list_sources:
            print("No sources to process. Encountered error with API")
        else:
            for source in list_sources:
                if (source_id := add_data_to_db(source)) != -1:
                    list_source_ids.append(source_id)
                else:
                    print("Error adding source to DB", str(source))
            update_subscribers(list_source_ids)
            self.page_number += 1

        print("NewsAPI Aggregator Daemon task finished")
