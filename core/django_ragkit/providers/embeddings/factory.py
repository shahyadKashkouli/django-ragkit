from django_ragkit.providers.embeddings.ollama import OllamaEmbeddingProvider
from django.conf import settings
def get_embedding_provider():
    provider = settings.RAGKIT["EMBEDDING"]["PROVIDER"]
    if provider == "ollama":
        return OllamaEmbeddingProvider()
    raise ValueError(f"Unknown embedding provider: {provider}")