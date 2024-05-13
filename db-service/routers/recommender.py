from fastapi import APIRouter, Depends, HTTPException
from models.utils.constants import RECOMMENDER_HOST
from routers.user import auth_manager
from models.utils.funcs import Response, get_data_from_api
from utils import change_db_id_to_str
from routers.annotator import get_posts_by_query


recommender_router = APIRouter(prefix="/recommender")


@recommender_router.get("/get-recommendations")
def get_recommendations(page: int, limit: int = 5, query: str = "", user=Depends(auth_manager)):
    if not query:
        if (
            recommendations := get_data_from_api(
                RECOMMENDER_HOST,
                "recommender/get-recommendations",
                {"user_id": user["id"], "limit": limit, "page": page},
            )
        ) == Response.FAILURE:
            raise HTTPException(status_code=400, detail="Could not get recommendations")
    else:
        recommendations = {
            "list_recommendations": get_posts_by_query(query, limit, page - 1),
            "message": "Retrieved posts by query",
        }
        

    recommendations["list_recommendations"] = list(
        map(change_db_id_to_str, recommendations["list_recommendations"])
    )
    return recommendations
