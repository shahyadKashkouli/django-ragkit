from abc import ABC, abstractmethod
from django.conf import  settings
from ..shared.base_provider import BaseProvider


class BaseEmbeddingProvider(BaseProvider):
    settings_key = "EMBEDDING"
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return the embedding vector for a single text."""
        raise NotImplementedError


    @property
    def dimension(self):
        return self.config["DIMENSION"]

