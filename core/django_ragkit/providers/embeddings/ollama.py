from .base_embeddings import BaseEmbeddingProvider
import requests


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    DEFAULT_CONFIG = {
        "BASE_URL": "http://localhost:11434",
    }
    MODELS = {
        "bge-m3": {
            "dimension": 1024,
        },
    }

    def embed(self, text: str) -> list[float]:
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={
                "model": self.model,
                "input": text,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["embeddings"][0]
