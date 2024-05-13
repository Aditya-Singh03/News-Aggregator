from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models.post import Post
from models.user import Preferences
from models.utils.funcs import get_data_from_api, add_data_to_api, Response
from models.utils.constants import DB_HOST
from models.recommendation import RecommendationQuery, PostRecommendation
from recommender.preferences import get_topic_recommendations
from tqdm import tqdm
from bing_image_urls import bing_image_urls


recommender_router = APIRouter(prefix="/recommender")


@recommender_router.get("/get-recommendations")
async def get_recommendations(_: Request, user_id: str, limit: int, page: int):
    print(f"Received request for recommendations for user: {user_id}")

    if (user := get_data_from_api(DB_HOST, "user/get-preferences", {"user_id": user_id})) == Response.FAILURE:
        raise HTTPException(status_code=404, detail="User not found")

    user_prefs = Preferences(preferences=user["preferences"])
    posts_pull_limit = limit * 2

    if (
        recommendations_json := get_data_from_api(
            DB_HOST,
            "recommendation/get-recommendations",
            {"limit": posts_pull_limit, "page": page},
        )
    ) == Response.FAILURE:
        raise HTTPException(status_code=404, detail="Recommendations not found")

    recommendations = [PostRecommendation(**rec) for rec in recommendations_json["recommendations"]]

    user_topics_dt = dict()
    for rec in recommendations:
        user_topics_dt[rec.post_id] = len(set(user_prefs.preferences) & set(rec.topics))

    sorted_user_posts = sorted(user_topics_dt.items(), key=lambda x: x[1], reverse=True)
    all_post_ids = [post_id for post_id, _ in sorted_user_posts]

    user_recom_posts: List[Post] = []

    for post_id in all_post_ids:
        if (post_json := get_data_from_api(DB_HOST, "annotator/get-post", {"post_id": post_id})) != Response.FAILURE:
            user_recom_posts.append(Post(**post_json["post"]))

        if len(user_recom_posts) == limit:
            break

    # For now, put bing media if media is not available
    for post in user_recom_posts:
        if not post.media:
            post.media = bing_image_urls(post.title, limit=1)[0]

    return {
        "message": "Recommendation sent",
        "list_recommendations": jsonable_encoder(user_recom_posts),
    }


@recommender_router.post("/add-recommendations")
async def add_recommendations(
    _: Request,
    background_tasks: BackgroundTasks,
    recommendation_query: RecommendationQuery,
):
    print("Received request to add recommendations")
    background_tasks.add_task(process_posts, recommendation_query)
    return {"message": "Recommendation process started"}


def process_posts(recommendation_query: RecommendationQuery):
    list_posts: List[Post] = []

    for post_id in tqdm(recommendation_query.post_ids, desc="Fetching posts"):
        if (post_json := get_data_from_api(DB_HOST, "annotator/get-post", {"post_id": post_id})) != Response.FAILURE:
            list_posts.append(Post(**post_json["post"]))

    posts_recommendations = get_topic_recommendations(list_posts)
    for post_recomm in posts_recommendations:
        add_data_to_api(DB_HOST, "recommendation/add-recommendation", post_recomm)
