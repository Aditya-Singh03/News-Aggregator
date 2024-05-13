from dotenv import dotenv_values
import os
from pymongo import MongoClient
from tqdm import tqdm
from bing_image_urls import bing_image_urls
import requests

config = dotenv_values(dotenv_path=os.path.join("db-service", ".env"))

client = MongoClient(config["ATLAS_URI"])


def add_info_to_posts():
    post_collection = client["annotator"]["posts"]
    source_collection = client["aggregator"]["sources"]

    for post in tqdm(
        post_collection.find(),
        desc="Adding media and date to posts",
        total=post_collection.count_documents(filter={}),
    ):
        source_ids = post["source_ids"]

        for source_id in source_ids:
            if (source := source_collection.find_one({"_id": source_id})) is not None:
                media = source["media"]
                date = source["date"]

                if not media.startswith("http"):
                    media = bing_image_urls(source["link"], limit=1)[0]

                post_collection.update_one(
                    {"_id": post["_id"]}, {"$set": {"media": media}}
                )

                post_collection.update_one(
                    {"_id": post["_id"]}, {"$set": {"date": date}}
                )

                break


def get_all_post_ids():
    post_collection = client["annotator"]["posts"]
    return [post["_id"] for post in post_collection.find()]


def add_recomendations():
    post_ids = get_all_post_ids()
    requests.post(
        f"http://localhost:8030/recommender/add-recommendations",
        json={"post_ids": post_ids},
    )


def search_index():
    llm_collection = client["llm"]["analyses"]
    result = llm_collection.aggregate(
        [
            {
                "$search": {
                    "index": "llm-post-query",
                    "text": {"query": "video game", "path": {"wildcard": "*"}},
                }
            },
            {"$skip": 1},
            {"$limit": 1},
            {"$project": {"_id": 0, "post_id": 1}},
        ]
    )
    print(list(result))


def remove_post(post_id):
    post_collection = client["annotator"]["posts"]
    recommendation_collection = client["recommendation"]["recommendations"]
    llm_collection = client["llm"]["analyses"]
    aggregation_collection = client["aggregator"]["sources"]

    recommendation_collection.delete_one({"post_id": post_id})
    llm_collection.delete_one({"post_id": post_id})

    for source_id in post_collection.find_one({"_id": post_id})["source_ids"]:
        aggregation_collection.delete_one({"_id": source_id})

    post_collection.delete_one({"_id": post_id})


if __name__ == "__main__":
    # post_ids = get_all_post_ids()
    # add_info_to_posts()
    # add_recomendations()
    # search_index()
    remove_post("e4313838-378a-43fb-be26-fe8f41a0eff4")
