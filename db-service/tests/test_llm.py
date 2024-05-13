from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from models.post import Post
from models.llm import PostAnalysis
from main import app
import mock
from utils import get_mongo_client

client = TestClient(app)
annotator_client = get_mongo_client()["annotator_test"]

post = Post(
    title="random",
    source_ids=["random"],
    topics=["random"],
)
post_analysis = PostAnalysis(
    post_id=post.id,
    completion={
        "title": "random",
        "summary": "random",
    },
)


@mock.patch("routers.llm.annotator_client", get_mongo_client()["annotator_test"])
@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_add_analysis():
    annotator_client["posts"].insert_one(jsonable_encoder(post))
    response = client.post("/llm/add-analysis", json=jsonable_encoder(post_analysis))
    assert response.status_code == 200


@mock.patch("routers.llm.annotator_client", get_mongo_client()["annotator_test"])
@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_add_analysis_duplicate():
    post_analysis_json = jsonable_encoder(post_analysis)
    post_analysis_json["post_id"] = "random"
    response = client.post("/llm/add-analysis", json=jsonable_encoder(post_analysis))
    assert response.status_code == 400


@mock.patch("routers.llm.annotator_client", get_mongo_client()["annotator_test"])
@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_add_analysis_no_post():
    post_analysis_json = jsonable_encoder(post_analysis)
    post_analysis_json["post_id"] = "random"
    response = client.post("/llm/add-analysis", json=post_analysis_json)
    assert response.status_code == 400


@mock.patch("routers.llm.annotator_client", get_mongo_client()["annotator_test"])
@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_get_analysis():
    response = client.get(f"/llm/get-analysis?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.llm.llm_client", get_mongo_client()["llm_test"])
def test_get_analysis_no_post():
    response = client.get("/llm/get-analysis?post_id=random")
    assert response.status_code == 404
