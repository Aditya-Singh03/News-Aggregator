from typing import List
from bundle.models.bert.constants import BERT_MODEL_PATH


def create_model(documents: List[str]):
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    topic_model = BERTopic(verbose=True, embedding_model=embedding_model)
    topic_model.fit(documents)

    return topic_model


def save_model(topic_model):
    topic_model.save(BERT_MODEL_PATH, save_embedding_model=False)


def load_model(saved_model_path):
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return BERTopic.load(saved_model_path, embedding_model=embedding_model)
