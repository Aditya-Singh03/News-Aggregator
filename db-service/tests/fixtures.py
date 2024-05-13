import pytest
from utils import get_mongo_client


@pytest.fixture(autouse=True, scope='session')
def clean_db():
    get_mongo_client().drop_database("llm_test")
    get_mongo_client().drop_database("recommendation_test")
    get_mongo_client().drop_database("annotator_test")
    get_mongo_client().drop_database("aggregator_test")
    get_mongo_client().drop_database("user_test")
    yield


