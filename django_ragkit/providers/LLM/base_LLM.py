from abc import abstractmethod
from django_ragkit.providers.shared.base_provider import BaseProvider


class BaseLLMProvider(BaseProvider):
    settings_key = "LLM"

    @abstractmethod
    def generate_response(self, prompt) -> str:
        raise NotImplementedError
