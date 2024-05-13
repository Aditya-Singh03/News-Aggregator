from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from routers.observer import update_subscribers
from main import app

client = TestClient(app)


def test_post_sub():
    sub = Subscriber(ip_address="123456789", port=1000)
    response = client.post("/observer/subscribe", json=jsonable_encoder(sub))
    assert response.status_code == 200
    assert response.json() == {"message": "Observer subscribed"}

    sub2 = Subscriber(ip_address="123456789", port=1000)
    response = client.post("/observer/subscribe", json=jsonable_encoder(sub2))
    assert response.status_code == 400


def test_get_sub():
    response = client.get("/observer/subscribers")
    assert response.status_code == 200
    assert "subscribers" in response.json() and type(response.json()["subscribers"]) is list


def test_update_sub_fail(capsys):
    update_subscribers(["random"])
    captured = capsys.readouterr()
    assert "Could not send update to" in captured.out
