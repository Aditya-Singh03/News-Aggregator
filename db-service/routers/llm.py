from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models.llm import PostAnalysis
from routers.annotator import annotator_client
from utils import get_mongo_client, change_db_id_to_str

llm_router = APIRouter(prefix="/llm")
llm_client = get_mongo_client()["llm"]


@llm_router.post("/add-analysis")
async def add_analysis(_: Request, post_analysis: PostAnalysis = Body(...)):
    if llm_client["analyses"].find_one({"id": post_analysis.id}):
        raise HTTPException(
            status_code=400, detail="Analysis with same id already exists"
        )
    elif llm_client["analyses"].find_one({"post_id": post_analysis.post_id}):
        raise HTTPException(
            status_code=400, detail="Analysis with same post_id already exists"
        )
    elif annotator_client["posts"].find_one({"_id": post_analysis.post_id}) is None:
        raise HTTPException(status_code=400, detail="Post with post_id does not exist")

    analysis_data = jsonable_encoder(post_analysis)
    res_analysis = llm_client["analyses"].insert_one(analysis_data)

    return {
        "message": "Added title",
        "title_id": str(res_analysis.inserted_id),
    }


@llm_router.get("/get-analysis")
async def get_summary(post_id: str):
    if not (analysis := llm_client["analyses"].find_one({"post_id": post_id})):
        raise HTTPException(status_code=404, detail="Analysis not found")
    return change_db_id_to_str(analysis)
