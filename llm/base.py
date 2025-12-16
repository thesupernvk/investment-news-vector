from abc import ABC, abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def embed(self, text: str) -> list:
        pass

    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass
