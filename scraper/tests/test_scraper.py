from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from main import app

client = TestClient(app)


def test_get_scrape():
    response = client.get("/scraper/get-scrape-data", params={"link": "badurl.bad"})
    assert response.status_code == 400

    response = client.get("/scraper/get-scrape-data", params={"link": "https://en.wikipedia.org/wiki/New_York_City"})
    assert response.status_code == 200
    assert "content" in response.json()
