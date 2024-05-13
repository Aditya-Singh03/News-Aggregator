from collections import defaultdict
from typing import List

from bundle.models.base_model import BaseModel
from bundle.models.bert.constants import BERT_MODEL_PATH
from bundle.models.bert.train import load_model

TOPIC_THRESHOLD = 0.3


class BERTModel(BaseModel):
    def __init__(self, documents: List[str], num_clusters) -> None:
        super().__init__(documents, num_clusters)
        self.bert_model = load_model(BERT_MODEL_PATH)

    def create_vector(self, document: str) -> List[float]:
        return document

    def cluster(self) -> tuple[dict[int, List[int]], dict[int, List[str]]]:
        pred_topics, probs = self.bert_model.transform(self.documents)

        clusters = defaultdict(list)
        dt_topics = dict()

        for i, (topic, prob) in enumerate(zip(pred_topics, probs)):
            if prob >= TOPIC_THRESHOLD:
                clusters[topic].append(i)

                if topic not in dt_topics:
                    dt_topics[topic] = [
                        keyword for keyword, _ in self.bert_model.get_topic(topic)
                    ]

        return clusters, dt_topics
