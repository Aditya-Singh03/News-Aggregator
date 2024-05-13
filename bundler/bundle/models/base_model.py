from typing import List


class BaseModel:
    def __init__(self, documents: List[str], num_clusters) -> None:
        self.documents = documents
        self.num_clusters = num_clusters
        self.corpus = [self.create_vector(doc) for doc in documents]

    def create_vector(self, document: str) -> List[float]:
        raise NotImplementedError("create_vector method is not implemented")

    def cluster(self) -> tuple[dict[int, List[int]], dict[int, List[str]]]:
        raise NotImplementedError("cluster method is not implemented")
