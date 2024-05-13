import os
from pathlib import Path

FILE_DIR = os.path.dirname(__file__)
PATH_TO_DB_DIR = os.path.join(FILE_DIR, "social-animal")


# Source: https://www.kaggle.com/datasets/socialanimal/social-animal-10k-articles-with-text-and-nlp-data/data?select=articles.csv
def get_social_news_data():
    path_to_files = os.path.join(PATH_TO_DB_DIR, "text")
    pathlist = Path(path_to_files).glob("*.txt")
    return [fpath.read_text(encoding="utf-8") for fpath in pathlist]
