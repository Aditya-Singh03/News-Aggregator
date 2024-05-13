from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.recommendation import PostRecommendation
from utils import get_mongo_client

recommendation_router = APIRouter(prefix="/recommendation")
recommendation_client = get_mongo_client()["recommendation"]


@recommendation_router.post("/add-recommendation")
async def add_recommendation(recommendation: PostRecommendation = Body(...)):
    if recommendation_client["recommendations"].find_one(
        {"post_id": recommendation.post_id}
    ):
        raise HTTPException(
            status_code=400, detail="Recommendation already exists for this post"
        )

    recommendation_dict = jsonable_encoder(recommendation)

    added_recommendation = recommendation_client["recommendations"].insert_one(
        recommendation_dict
    )

    return {
        "message": "Recommendation added",
        "recommendation_id": str(added_recommendation.inserted_id),
    }


@recommendation_router.get("/get-recommendations")
async def get_recommendations(limit: int, page: int):
    if (
        recommendations := recommendation_client["recommendations"]
        .find()
        .sort({"_id": -1})
        .skip((page - 1) * limit)
        .limit(limit)
    ) is not None:
        return {
            "recommendations": list(recommendations),
            "message": "Recommendations retrieved",
        }

    raise HTTPException(status_code=404, detail="Recommendations not found")
