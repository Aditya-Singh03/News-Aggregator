from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
import mock
from models.user import (
    RegisterUser,
    LoginUser,
    Token,
    Preferences,
    UserVotes,
    UpdateUser,
)

client = TestClient(app)


reg_user = RegisterUser(
    email_address="test@email.com",
    password="password1",
    username="test",
    avatar=1,
)

login_user = LoginUser(
    email_address="test@email.com",
    password="password1",
)

update_user = UpdateUser(
    email_address="test@gmail.com", 
    password="password1",
    username="testUpdated",
    avatar=2,
)

preferences = Preferences(
    preferences=["test1", "test2"],
)

user_token = ""

#Below are the endpoints for which coverage tests are to be written
@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_register_user():
    response = client.post("/user/register", json=jsonable_encoder(reg_user))
    assert response.status_code == 200
    assert "token" in response.json() and "message" in response.json()
    global user_token
    user_token = response.json()["token"]
    user_json = jsonable_encoder(reg_user)
    response = client.post("/user/register", json=user_json)
    assert response.status_code == 401
    user_json['_id'] = '1'
    response = client.post("/user/register", json=user_json)
    assert response.status_code == 401
    user_json['username'] = ''
    response = client.post("/user/register", json=user_json)
    assert response.status_code == 401


@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_update_user():
    response = client.put("/user/update-user", json=jsonable_encoder(update_user))
    assert response.status_code == 200
    assert "message" in response.json()
    user_json = jsonable_encoder(reg_user)
    response = client.put("/user/update-user", json=user_json)
    assert response.status_code == 401
    user_json['_id'] = '1'
    response = client.put("/user/update-user", json=user_json)
    assert response.status_code == 401
    user_json['username'] = ''
    response = client.put("/user/update-user", json=user_json)
    assert response.status_code == 401

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_login_user():
    response = client.post("/user/login", json=jsonable_encoder(login_user))
    assert response.status_code == 200
    assert "token" in response.json() and "message" in response.json()

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_view_user():
    response = client.get("/user/view", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert "message" in response.json()

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_get_user():
    response = client.get("/user/get-user?user_id=1")
    assert response.status_code == 200
    assert "message" in response.json()

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_get_all_users():
    response = client.get("/user/get-all-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_add_preferences():
    response = client.post("/user/add-preferences", json=jsonable_encoder(preferences))
    assert response.status_code == 200
    assert "message" in response.json()

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_get_preferences():
    response = client.get("/user/get-preferences?user_id=1")
    assert response.status_code == 200
    assert "message" in response.json()

@mock.patch("routers.user.user_client", get_mongo_client()["user_test"])
def test_add_duplicate_preferences():
    response = client.post("/user/add-preferences", json=jsonable_encoder(preferences))
    assert response.status_code == 401
    assert "detail" in response.json()



