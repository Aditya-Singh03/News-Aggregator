import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.recommender import recommender_router
from recommender.collabfilter import CollabFilteringDaemon
import sys

RECOMMENDER_DELAY = 60 * 60  # 1 hour


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(CollabFilteringDaemon(RECOMMENDER_DELAY).start_daemon())
    yield


origins = ["*"]
app = FastAPI(title="News Recommender", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommender_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


def debug():
    from routers.recommender import process_posts
    from models.recommendation import RecommendationQuery

    recommendation_query = RecommendationQuery(
        post_ids=[
            "a032af0c-b310-446f-8ac8-e11c0be436d5",
            "c17d25a9-6317-41fa-b8cf-124043abef56",
        ]
    )

    process_posts(recommendation_query)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug()
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8030, reload=True, workers=1)
