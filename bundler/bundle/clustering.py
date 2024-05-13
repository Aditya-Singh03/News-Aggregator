from typing import List
from bundle.preprocess import preprocess
from bundle.models.base_model import BaseModel
from bundle.models.lda import LDAModel
from bundle.models.lsi import LSIModel
from bundle.models.bert.bert_topic import BERTModel

get_class = lambda x: globals()[x]


def cluster_by_topic(model_name: str, documents: List[str], num_clusters: int):
    processed_docs = (
        [preprocess(doc) for doc in documents] if model_name != "bert" else documents
    )
    model: BaseModel = get_class(f"{model_name.upper()}Model")(
        processed_docs, num_clusters
    )
    return model.cluster()
