from enum import Enum
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import requests


class Response(Enum):
    SUCCESS = 1
    FAILURE = -1


def subscribe_to_publisher(
    subscriber_ip, subscriber_port, publisher_ip, publisher_port
) -> Response:
    url = f"http://{publisher_ip}:{publisher_port}/observer/subscribe"
    status = Response.SUCCESS

    try:
        response = requests.post(
            url, json={"ip_address": subscriber_ip, "port": subscriber_port}, timeout=5
        )
    except requests.exceptions.RequestException as e:
        print("Could not subscribe to publisher", e)
        status = Response.FAILURE

    if response.status_code == 200:
        print("Subscribed to publisher")
    else:
        print("Failed to subscribe to publisher,", response.json())
        status = Response.FAILURE

    return status


def add_data_to_api(host: str, endpoint: str, data_model: BaseModel) -> Response:
    url = f"http://{host}/{endpoint}"
    status = Response.SUCCESS

    try:
        response = requests.post(url, json=jsonable_encoder(data_model), timeout=15)
    except requests.exceptions.RequestException:
        print(f"Could not send data to service due to timeout")
        status = Response.FAILURE
    else:
        if response.status_code != 200:
            print(f"Received status code {response.status_code} from service")
            status = Response.FAILURE

    return status


def get_data_from_api(
    host: str, endpoint: str, params: dict | BaseModel = None
) -> dict | Response:
    if params is None:
        params = {}

    url = f"http://{host}/{endpoint}"
    status = Response.SUCCESS

    try:
        response = requests.get(url, params=jsonable_encoder(params), timeout=15)
    except requests.exceptions.RequestException:
        print(f"Could not get data from service due to timeout")
        status = Response.FAILURE
    else:
        if response.status_code != 200:
            print(f"Received status code {response.status_code} from service")
            status = Response.FAILURE

    return response.json() if status == Response.SUCCESS else Response.FAILURE
