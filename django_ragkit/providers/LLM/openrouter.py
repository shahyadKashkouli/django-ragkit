import json
import requests

from django_ragkit.providers.LLM.base_LLM import BaseLLMProvider


class OpenRouterLLMProvider(BaseLLMProvider):

    def generate_response(self, prompt):

        if not isinstance(prompt, str):
            prompt = json.dumps(
                prompt,
                ensure_ascii=False,
            )

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]