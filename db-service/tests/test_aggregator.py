from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
from models.source import Source
import mock

client = TestClient(app)


@mock.patch("routers.aggregator.aggregator_client", get_mongo_client()["aggregator_test"])
def test_aggregator():

    #Check for failure in getting the recommendation

    """
class Source(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str = ""
    link: str = ""
    media: str = ""
    author: str = ""
    date: str = ""
    """

    source_body = Source(
        title="2",
        link="2",
        media="2",
        author="2",
        date="2",
    )
    response = client.post("aggregator/add-aggregation", json=jsonable_encoder(source_body))
    assert response.status_code == 200
    
    response = client.post("aggregator/add-aggregation", json=jsonable_encoder(source_body))
    assert response.status_code == 400

    response = client.get("aggregator/get-aggregation?source_id=123")
    assert response.status_code == 200

    response = client.get("aggregator/get-all-aggregations?limit=10")
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
