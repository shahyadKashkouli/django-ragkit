import json
from django_ragkit.providers.LLM.base_LLM import BaseLLMProvider
import requests


class OllamaLLMProvider(BaseLLMProvider):
    DEFAULT_CONFIG = {
        "BASE_URL": "http://localhost:11434",
    }
    MODELS = {
        "qwen3:4b": {
        },
    }

    def generate_response(self, prompt):
        prompt = json.dumps(prompt, ensure_ascii=False)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        return data["response"]
