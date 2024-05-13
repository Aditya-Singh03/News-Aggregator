from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.pub_sub import Subscriber
from main import app
from utils import get_mongo_client
from models.recommendation import PostRecommendation
from models.user import RegisterUser
import mock
from routers.user import auth_manager
from models.utils.funcs import Response

test_user = {"id": "f8a21c66-fdd2-4f3a-8eff-229a18d747e4"}
app.dependency_overrides[auth_manager] = lambda: test_user
client = TestClient(app)

def test_recommender(mocker):
    
    mocker.patch(
        "routers.recommender.get_data_from_api",
        return_value=Response.FAILURE,
    )

    # Check for failure in getting the recommendation
    response = client.get("/recommender/get-recommendations?page=1")
    assert response.status_code == 400

    mocker.patch(
        "routers.recommender.get_data_from_api",
        return_value={
            "list_recommendations": [],
            "message": "Retrieved posts by query",
        },
    )
    mocker.patch("routers.recommender.get_posts_by_query", return_value=[])
    response = client.get("/recommender/get-recommendations?page=1&query=x")
    assert response.status_code == 200
