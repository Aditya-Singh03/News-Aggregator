from typing import List
from fastapi import APIRouter, Body, Request, BackgroundTasks
from tqdm import tqdm
from models.llm import PostQuery, PostsAnalysisQuery
from models.utils.constants import DB_HOST, LLM_HOST, SCRAPER_HOST
from models.pub_sub import AggregatorMessage
from models.utils.funcs import add_data_to_api, get_data_from_api, Response
from models.post import Post
from models.source import Source
from models.scraper import ScrapeQuery, ScrapeData
from bundle.clustering import cluster_by_topic
from datetime import datetime
from bundle.collage import make_collage

subscriber_router = APIRouter(prefix="/subscriber")
MODEL_NAME = "bert"


@subscriber_router.post("/update")
async def update_from_publisher(
    _: Request,
    background_tasks: BackgroundTasks,
    message: AggregatorMessage = Body(...),
):
    print(f"Received message: {message}")
    add_background_task(background_tasks, message.source_ids)
    return {"message": "Annotations in progress"}


def add_background_task(background_tasks: BackgroundTasks, list_source_ids: list[str]):
    background_tasks.add_task(process_sources, list_source_ids)


def process_sources(list_source_ids: list[str]):
    if not list_source_ids:
        print("No sources to process")
        return

    documents: List[str] = []
    sources: List[Source] = []

    # FIXME: extract parts of this code into a function
    for source_id in tqdm(list_source_ids, desc="Processing sources"):
        if (
            source_data := get_data_from_api(
                DB_HOST, "aggregator/get-aggregation", {"source_id": source_id}
            )
        ) != Response.FAILURE:
            source = Source(**source_data["source"])
            scrape_query = ScrapeQuery(link=source.link)

            if (
                scraped_json := get_data_from_api(
                    SCRAPER_HOST, "scraper/get-scrape-data", scrape_query
                )
            ) != Response.FAILURE:
                scrape_data = ScrapeData(**scraped_json)
                documents.append(scrape_data.content)
                sources.append(source)

    if documents:
        print("Clustering sources")
        assert len(documents) == len(
            sources
        ), "Documents and sources length should be equal"

        cluster_topics, idx_to_topic = cluster_by_topic(
            MODEL_NAME, documents, num_clusters=len(sources)
        )

        list_post_queries: List[PostQuery] = []

        for cluster_idx, list_source_idx in cluster_topics.items():
            cluster_sources: List[Source] = []

            for source_idx in list_source_idx:
                source = sources[source_idx]
                cluster_sources.append(source)

            post = Post(
                source_ids=[source.id for source in cluster_sources],
                topics=list(filter(None, idx_to_topic[cluster_idx])),
                date=get_min_date([source.date for source in cluster_sources]),
                media=make_collage([source.media for source in cluster_sources]),
            )

            if add_data_to_api(DB_HOST, "annotator/add-post", post) != Response.FAILURE:
                cur_documents = [
                    documents[source_idx] for source_idx in list_source_idx
                ]
                text_content = "\n ".join(cur_documents)
                list_post_queries.append(PostQuery(post_id=post.id, text=text_content))

        if list_post_queries:
            llm_post_analysis = PostsAnalysisQuery(post_queries=list_post_queries)
            add_data_to_api(LLM_HOST, "llm/add-analysis", llm_post_analysis)


def get_min_date(list_dates: List[str]) -> str:
    DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    list_dt = [datetime.strptime(date, DT_FORMAT) for date in list_dates if date]
    return min(list_dt).strftime(DT_FORMAT)
