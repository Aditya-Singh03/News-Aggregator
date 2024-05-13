from fastapi import APIRouter, Body, HTTPException
from utils import get_mongo_client, change_db_id_to_str
from models.source import Source
from fastapi.encoders import jsonable_encoder


aggregator_router = APIRouter(prefix="/aggregator")
aggregator_client = get_mongo_client()["aggregator"]


@aggregator_router.post("/add-aggregation")
async def put_aggregations(source: Source = Body(...)):
    # Check for duplicates with the same link
    if aggregator_client["sources"].find_one({"link": source.link}):
        raise HTTPException(
            status_code=400, detail="Source with same link already exists"
        )

    source_data = jsonable_encoder(source)
    res_source = aggregator_client["sources"].insert_one(source_data)
    return {
        "message": "Added text aggregation",
        "source_id": str(res_source.inserted_id),
    }


@aggregator_router.get("/get-aggregation")
async def get_aggregation(source_id: str):
    source = get_source(source_id)
    return {"message": "Retrieved aggregations", "source": jsonable_encoder(source)}


@aggregator_router.get("/get-all-aggregations")
async def get_all_aggregations(limit: int):
    return {
        "message": "Retrieved aggregations",
        "list_sources": get_all_sources(limit),
    }


def get_source(post_id: str):
    source = aggregator_client["sources"].find_one({"_id": post_id})
    return change_db_id_to_str(source)


def get_all_sources(limit: int):
    list_sources = aggregator_client["sources"].find().limit(limit)
    return list(map(change_db_id_to_str, list_sources))
