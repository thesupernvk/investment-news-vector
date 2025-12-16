from abc import ABC, abstractmethod
from typing import List, Dict

class VectorStore(ABC):

    @abstractmethod
    def add(self, ids: List[str], embeddings: List[list], documents: List[str], metadatas: List[Dict]):
        pass

    @abstractmethod
    def similarity_search(self, query_embedding: list, k: int):
        pass

    @abstractmethod
    def url_exists(self, url: str) -> bool:
        pass

    @abstractmethod
    def content_hash_exists(self, content_hash: str) -> bool:
        pass
