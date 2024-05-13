from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from models.llm import Prompt, PostCompletion, PostsAnalysisQuery, PostQuery
from main import app

client = TestClient(app)


def test_prompt_empty():
    response = client.post(
        "/llm/prompt",
        json=jsonable_encoder(Prompt(prompt="", query="")),
    )
    assert response.status_code == 400


def test_prompt_result(mocker):
    mocker.patch("routers.llm.generate_text_from_ollama", return_value="test")
    response = client.post(
        "/llm/prompt",
        json=jsonable_encoder(Prompt(prompt="test", query="test")),
    )
    assert response.status_code == 200


def test_generate_analysis(mocker):
    mocker.patch("routers.llm.ollama_keep_alive", return_value=None)

    mocker.patch(
        "routers.llm.generate_text_from_ollama",
        return_value=PostCompletion(title="test", summary="test"),
    )

    mocker.patch("routers.llm.add_data_to_api", return_value=None)

    response = client.post(
        "/llm/add-analysis",
        json=jsonable_encoder(
            PostsAnalysisQuery(post_queries=[PostQuery(post_id="1", text="test")])
        ),
    )
    assert response.status_code == 200
