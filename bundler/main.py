import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.utils.funcs import subscribe_to_publisher
from routers.subscriber import subscriber_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    subscribe_to_publisher(
        os.getenv("SUBSCRIBER_IP", "localhost"),
        8020,
        os.getenv("PUBLISHER_IP", "localhost"),
        8010,
    )
    yield


origins = ["*"]
app = FastAPI(title="News Annotator", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscriber_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


def train_bert():
    from bertopic import BERTopic

    from bundle.models.bert.constants import FILE_DIR
    from bundle.models.bert.data.social_animal_driver import get_social_news_data
    from bundle.models.bert.train import create_model, load_model, save_model

    prev_topic_model = load_model(
        os.path.join(os.path.join(FILE_DIR, "saved_models"), "bert_model_all_news.bin")
    )

    list_documents = get_social_news_data()
    cur_topic_model = create_model(list_documents)

    topic_model = BERTopic.merge_models([prev_topic_model, cur_topic_model])
    save_model(topic_model)


def evaluate_bert():
    import gensim.corpora as corpora
    from gensim.models.coherencemodel import CoherenceModel
    from tqdm import tqdm

    from bundle.models.bert.constants import FILE_DIR
    from bundle.models.bert.data.all_news_driver import get_all_news_data
    from bundle.models.bert.data.social_animal_driver import get_social_news_data
    from bundle.models.bert.train import load_model

    topic_model = load_model(os.path.join(os.path.join(FILE_DIR, "saved_models"), "bert_model.bin"))

    cleaned_docs = get_social_news_data() + get_all_news_data()

    vectorizer = topic_model.vectorizer_model
    analyzer = vectorizer.build_analyzer()
    tokens = [analyzer(doc) for doc in tqdm(cleaned_docs)]

    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]
    topics = topic_model.get_topics()
    topics.pop(-1, None)

    topic_words = [[word for word, _ in topic_model.get_topic(topic) if word != ""] for topic in topics]
    topic_words = [
        [words for words, _ in topic_model.get_topic(topic)] for topic in range(len(set(topics)) - 1)
    ]
    topic_words = [[topic_w for topic_w in topic if topic_w] for topic in topic_words]
    topic_words = list(filter(None, topic_words))

    coherence_model = CoherenceModel(
        topics=topic_words,
        corpus=corpus,
        dictionary=dictionary,
        coherence="u_mass",
    )
    coherence = coherence_model.get_coherence()

    print(f"Coherence: {coherence}")


def debug():
    from bundle.collage import make_collage

    link = make_collage(
        [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Taka_Shiba.jpg/1200px-Taka_Shiba.jpg",
            "https://cdn.britannica.com/71/234471-050-093F4211/shiba-inu-dog-in-the-snow.jpg",
            "https://www.akc.org/wp-content/uploads/2017/11/Shiba-Inu-standing-in-profile-outdoors.jpg",
            "https://www.akc.org/wp-content/uploads/2017/11/Shiba-Inu-puppy-standing-outdoors.jpg",
        ]
    )

    print(link)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            debug()
        elif sys.argv[1] == "train":
            train_bert()
        elif sys.argv[1] == "evaluate":
            evaluate_bert()
        else:
            exit(1)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8020, reload=True, workers=1)
