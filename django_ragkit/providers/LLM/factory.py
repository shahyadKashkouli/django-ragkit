from django.conf import settings
from django_ragkit.providers.LLM.ollama import OllamaLLMProvider
from django_ragkit.providers.LLM.openrouter import OpenRouterLLMProvider


def get_LLM_provider():
    provider = settings.RAGKIT["LLM"]["PROVIDER"]
    if provider == "ollama":
        return OllamaLLMProvider()
    elif provider == "openrouter":
        return OpenRouterLLMProvider()
    raise ValueError(f"Unknown LLM provider: {provider}")