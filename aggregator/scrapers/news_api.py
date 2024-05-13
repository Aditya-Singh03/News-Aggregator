import requests
from sys import exit
from dotenv import load_dotenv
import os
from models.source import Source


load_dotenv()

if (NEWS_API_KEY := os.getenv("NEWS_API_KEY")) is None:
    print("API key not found. Please check your .env file.")
    exit(1)


def create_params(kwargs: dict):
    params = {}
    for key, value in kwargs.items():
        if value:
            params[key] = value
    return params


def call_everything(
    keywords,
    searchIn="",
    fromDate="",
    to="",
    language="en",
    sortBy="publishedAt",
    pageSize=5,
    page=1,
):
    url = "https://newsapi.org/v2/everything"
    try:
        response = requests.get(
            url,
            params=create_params(
                {
                    "q": keywords,
                    "apiKey": NEWS_API_KEY,
                    "searchIn": searchIn,
                    "from": fromDate,
                    "to": to,
                    "sortBy": sortBy,
                    "language": language,
                    "pageSize": pageSize,
                    "page": page,
                }
            ),
        )
        response.raise_for_status()
        response = cleanup(response.json())
        return parse_response(response)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return None


def call_top_headline(category=None, keyWords=None, pageSize=5, country="us", page=1):
    url = "https://newsapi.org/v2/top-headlines"
    try:
        response = requests.get(
            url,
            params=create_params(
                {
                    "q": keyWords,
                    "apiKey": NEWS_API_KEY,
                    "category": category,
                    "keyWords": keyWords,
                    "pageSize": pageSize,
                    "country": country,
                    "page": page,
                }
            ),
        )
        response.raise_for_status()
        response = cleanup(response.json())
        return parse_response(response)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return None


def cleanup(response):
    filtered_articles = []
    if "articles" in response:
        for article in response["articles"]:
            if article.get("title") != "[Removed]":
                filtered_articles.append(article)
    response["articles"] = filtered_articles
    return response


def parse_response(response):
    sources = []
    for article in response["articles"]:
        try:
            params = {
                "title": article.get("title"),
                "link": article.get("url"),
                "media": article.get("urlToImage"),
                "author": article.get("author"),
                "date": article.get("publishedAt"),
            }
            source = Source(**create_params(params))
        except Exception as exception_cur:
            print(f"Failed to parse article: {exception_cur}")
        else:
            sources.append(source)
    return sources


def test_calls():
    response = call_top_headline()

    if response is None:
        print("Failed to retrieve data")
        exit(1)

    print(f"Length of response: {len(response)}")
    for article in response:
        print(article.title)
