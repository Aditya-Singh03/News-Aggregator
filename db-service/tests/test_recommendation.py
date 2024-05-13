from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
from models.recommendation import PostRecommendation
import mock

client = TestClient(app)


@mock.patch("routers.recommendation.recommendation_client", get_mongo_client()["recommendation_test"])
def test_add_recommendation():
    post_recommendation = PostRecommendation(
        post_id="random",
        topics=["random"],
        date="random",
    )
    #Check for failure in getting the recommendation
    response = client.get("/recommendation/get-recommendation?limit=10&page=1")
    assert response.status_code == 404
    response = client.post("/recommendation/add-recommendation", json=jsonable_encoder(post_recommendation))
    assert response.status_code == 200
    response = client.post("/recommendation/add-recommendation", json=jsonable_encoder(post_recommendation))
    assert response.status_code == 400

    response = client.get("/recommendation/get-recommendations?limit=10&page=1")
    assert response.status_code == 200




# TODO change tests
# def test_post_sub():
#     sub = Subscriber(ip_address="123456789", port=1000)
#     response = client.post("/observer/subscribe", json=jsonable_encoder(sub))
#     assert response.status_code == 200
#     assert response.json() == {"message": "Observer subscribed"}

#     sub2 = Subscriber(ip_address="123456789", port=1000)
#     response = client.post("/observer/subscribe", json=jsonable_encoder(sub2))
#     assert response.status_code == 400


# def test_get_sub():
#     response = client.get("/observer/subscribers")
#     assert response.status_code == 200
#     assert "subscribers" in response.json() and type(response.json()["subscribers"]) is list


# def test_update_sub_fail(capsys):
#     update_subscribers(["random"])
#     captured = capsys.readouterr()
#     assert "Could not send update to" in captured.out
