from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from daemons.news_api_aggregator import NewsAPIAggDaemon
from routers.observer import observer_router, update_subscribers
from contextlib import asynccontextmanager
import asyncio

origins = ["*"]
AGGREGATION_DELAY = 60 * 60  # 1 hour


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(NewsAPIAggDaemon(AGGREGATION_DELAY).start_daemon())
    yield


app = FastAPI(title="News Annotator Aggregator", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(observer_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/test-update")
async def test_update():
    update_subscribers("test")
    return {"message": "Test update sent"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True, workers=1)
