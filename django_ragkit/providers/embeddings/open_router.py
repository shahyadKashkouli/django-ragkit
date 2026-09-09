from .base_embeddings import BaseEmbeddingProvider
import requests


class OpenRouterEmbeddingProvider(BaseEmbeddingProvider):

    def embed(self, text: str) -> list[float]:
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "input": text,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()
        print(data["data"][0]["embedding"])
        return data["data"][0]["embedding"]