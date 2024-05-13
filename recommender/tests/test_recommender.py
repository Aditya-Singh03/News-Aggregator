from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.recommendation import RecommendationQuery
from main import app

client = TestClient(app)


def test_get_recommendations():
    response = client.get("/recommender/get-recommendations", params={"user_id": "baduserid", "limit": 10, "page": 2})
    assert response.status_code == 404

    response = client.get(
        "/recommender/get-recommendations", params={"user_id": "01f98fe7-f86f-4f62-8440-5ed90ac3b502", "limit": 10, "page": 2}
    )
    assert response.status_code == 200
    assert (
        "message" in response.json()
        and "list_recommendations" in response.json()
        and response.json()["message"] == "Recommendation sent"
    )


def test_post_recommendations():
    rq = RecommendationQuery(post_ids=["cf3c5b6c-4ac0-4f8f-9195-575dbd463f95"])
    response = client.post("/recommender/add-recommendations", json=jsonable_encoder(rq))
    assert response.status_code == 200
    assert response.json() == {"message": "Recommendation process started"}
