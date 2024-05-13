from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from main import app
from models.source import Source
from models.pub_sub import AggregatorMessage
from models.scraper import ScrapeData

client = TestClient(app)

source = Source(
    title="test", link="test", media="test", author="test", date="2021-01-01T00:00:00Z"
)
scrape_data = ScrapeData(content="test")
message = AggregatorMessage(source_ids=[source.id], message="test")

cluster_ret = (
    {"test": [0]},
    {"test": ["test"]},
)


def patch_func(*args):
    api_url = args[1]
    if api_url == "aggregator/get-aggregation":
        return {"source": jsonable_encoder(source)}
    elif api_url == "scraper/get-scrape-data":
        return jsonable_encoder(scrape_data)
    else:
        return None


def test_update_from_publisher(mocker):
    mocker.patch("routers.subscriber.get_data_from_api", side_effect=patch_func)
    mocker.patch(
        "routers.subscriber.cluster_by_topic",
        return_value=cluster_ret,
    )

    response = client.post(
        "/subscriber/update",
        json=jsonable_encoder(message),
    )
    assert response.status_code == 200


def test_update_empty():
    message_json = jsonable_encoder(message)
    message_json["source_ids"] = []
    response = client.post(
        "/subscriber/update",
        json=message_json,
    )
    assert response.status_code == 200
