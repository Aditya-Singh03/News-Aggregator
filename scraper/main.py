from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.scraper import scraper_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


origins = ["*"]
app = FastAPI(title="News Annotator", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scraper_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8050, reload=True, workers=1)
