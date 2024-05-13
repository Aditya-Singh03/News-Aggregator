from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from main import app
from utils import get_mongo_client
from models.recommendation import PostRecommendation
from models.llm import PostAnalysis, PostCompletion
from models.post import Comment, Post
from routers.user import auth_manager
import mock


test_user = {"id": "f8a21c66-fdd2-4f3a-8eff-229a18d747e4"}
app.dependency_overrides[auth_manager] = lambda: test_user
client = TestClient(app)


post_recommendation = PostRecommendation(
    post_id="random",
    topics=["random"],
    date="random",
)

post = Post(
    source_ids=["random"],
    topics=["random"],
    summary="random",
    title="random",
    media="random",
    date="random",
    upvotes=0,
    downvotes=0,
)

post_analysis = PostAnalysis(
    post_id=post.id,
    completion=PostCompletion(
        title="random",
        summary="random",
    ),
)

comment = Comment(content="random", post_id=post.id, upvotes=0, downvotes=0)


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_add_post():
    response = client.post("/annotator/add-post", json=jsonable_encoder(post))
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_post(mocker):
    mocker.patch(
        "routers.annotator.get_llm_result_by_post_id",
        return_value=jsonable_encoder(post_analysis),
    )
    response = client.get(f"/annotator/get-post?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_post_query():
    response = client.get(f"/annotator/get-all-posts?query=summary")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_all_posts_query():
    response = client.get(f"/annotator/get-all-posts")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_all_posts():
    response = client.get("/annotator/get-all-posts")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_fail_remove_upvote_post():
    response = client.put(f"/annotator/remove-upvote-post?post_id={post.id}")
    assert response.status_code == 400


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_upvote_post():
    response = client.put(f"/annotator/upvote-post?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_upvote_post():
    response = client.put(f"/annotator/remove-upvote-post?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_fail_remove_downvote_post():
    response = client.put(f"/annotator/remove-downvote-post?post_id={post.id}")
    assert response.status_code == 400


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_downvote_post():
    response = client.put(f"/annotator/downvote-post?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_downvote_post():
    response = client.put(f"/annotator/remove-downvote-post?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_add_comment():
    response = client.post("/annotator/comment", json=jsonable_encoder(comment))
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_fail_remove_upvote_comment():
    response = client.put(f"/annotator/remove-upvote-comment?comment_id={comment.id}")
    assert response.status_code == 400


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_upvote_comment():
    response = client.put(f"/annotator/upvote-comment?comment_id={comment.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_upvote_comment():
    response = client.put(f"/annotator/remove-upvote-comment?comment_id={comment.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_fail_remove_downvote_comment():
    response = client.put(f"/annotator/remove-downvote-comment?comment_id={comment.id}")
    assert response.status_code == 400


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_downvote_comment():
    response = client.put(f"/annotator/downvote-comment?comment_id={comment.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_remove_downvote_comment():
    response = client.put(f"/annotator/remove-downvote-comment?comment_id={comment.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_comments():
    response = client.get(f"/annotator/get-comments?post_id={post.id}")
    assert response.status_code == 200


@mock.patch("routers.annotator.annotator_client", get_mongo_client()["annotator_test"])
def test_get_comment():
    response = client.get(f"/annotator/get-comment?comment_id={comment.id}")
    assert response.status_code == 200
