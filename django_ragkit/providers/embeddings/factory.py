from django_ragkit.providers.embeddings.ollama import OllamaEmbeddingProvider
from django.conf import settings

from django_ragkit.providers.embeddings.open_router import OpenRouterEmbeddingProvider


def get_embedding_provider():
    provider = settings.RAGKIT["EMBEDDING"]["PROVIDER"]
    if provider == "ollama":
        return OllamaEmbeddingProvider()
    elif provider == "openrouter":
        return OpenRouterEmbeddingProvider()
    raise ValueError(f"Unknown embedding provider: {provider}")