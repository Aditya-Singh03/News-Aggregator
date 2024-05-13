import sqlite3
import os

FILE_DIR = os.path.dirname(__file__)
PATH_TO_DB = os.path.join(FILE_DIR, "all-the-news.db")


# Source: https://components.one/datasets/all-the-news-articles-dataset/
def get_all_news_data():
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    print("Fetching data from database")
    res = cur.execute("SELECT content FROM longform").fetchall()
    print("Fetched data from database")

    return [r[0] for r in res if r[0] is not None]
