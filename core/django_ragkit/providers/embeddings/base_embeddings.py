from abc import ABC, abstractmethod

from ..shared.base_provider import BaseProvider


class BaseEmbeddingProvider(BaseProvider):
    settings_key = "EMBEDDING"
    MODELS = {}
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return the embedding vector for a single text."""
        raise NotImplementedError


    @property
    def dimension(self):
        return self.MODELS[self.model]["dimension"]

