from django.conf import settings
from django_ragkit.providers.LLM.ollama import OllamaLLMProvider


def get_LLM_provider():
    provider = settings.RAGKIT["LLM"]["PROVIDER"]
    if provider == "ollama":
        return OllamaLLMProvider()
    raise ValueError(f"Unknown LLM provider: {provider}")