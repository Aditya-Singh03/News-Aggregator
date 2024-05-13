from fastapi import FastAPI
from dotenv import dotenv_values
import uvicorn
from routers.user import user_router
from routers.annotator import annotator_router
from routers.aggregator import aggregator_router
from routers.recommender import recommender_router
from routers.llm import llm_router
from routers.recommendation import recommendation_router
from utils import get_mongo_client
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")
origins = ["*"]


app = FastAPI(title="News Annotator DB-Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(annotator_router)
app.include_router(aggregator_router)
app.include_router(recommender_router)
app.include_router(llm_router)
app.include_router(recommendation_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/clean-db")
async def clean_db():
    client = get_mongo_client()
    client.drop_database("user")
    client.drop_database("annotator")
    client.drop_database("llm")
    client.drop_database("recommendation")
    return {"message": "Databases cleaned"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
