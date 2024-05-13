import requests
import os
from fastapi.encoders import jsonable_encoder


def add_data_to_db(source_data):
    DB_HOST = os.getenv("DB_HOST", "localhost")
    db_url = f"http://{DB_HOST}:8000/aggregator/add-aggregation"

    encountered_error = False

    try:
        response = requests.post(db_url, json=jsonable_encoder(source_data), timeout=5)
    except requests.exceptions.RequestException:
        print(f"Could not send data to database service due to timeout")
        encountered_error = True
    else:
        if response.status_code != 200:
            print(f"Received status code {response.status_code} from database service")
            encountered_error = True

    resp_json = response.json() if not encountered_error else None
    return -1 if encountered_error else resp_json["source_id"]
