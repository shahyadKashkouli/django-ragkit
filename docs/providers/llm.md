# LLM Providers

Django RAGKit ships with built-in support for both local (**Ollama**) and cloud-based (**OpenRouter**) Large Language Models.

---

## Ollama (Local & Privacy-Focused)

[Ollama](https://ollama.com/) lets you run open-source large language models locally on your own machine or private server without sending data to external APIs.

### 1. Prerequisites

Download and start Ollama on your machine:

```bash
# Pull your desired model
ollama pull llama3.2
```

Ensure Ollama is running and accessible at `http://localhost:11434`.

### 2. Configuration in `settings.py`

```python title="settings.py"
RAGKIT = {
    # ...
    "LLM": {
        "PROVIDER": "ollama",
        "MODEL": "llama3.2",
        "BASE_URL": "http://localhost:11434",
    },
}
```

> [!TIP]
> **Docker Note**: If running Django inside Docker and Ollama on the host machine, set `"BASE_URL": "http://host.docker.internal:11434"`.

---

## OpenRouter (Cloud Multi-Model API)

[OpenRouter](https://openrouter.ai/) provides a unified OpenAI-compatible API to hundreds of AI models from OpenAI, Anthropic, Google, Meta, Mistral, and open-source contributors (including many free tier models).

### 1. Prerequisites

1. Sign up at [openrouter.ai](https://openrouter.ai/).
2. Create an API Key.
3. Add `LLM_API_KEY` to your `.env` file.

### 2. Configuration in `settings.py`

```python title="settings.py"
import os

RAGKIT = {
    # ...
    "LLM": {
        "PROVIDER": "openrouter",
        "MODEL": "nex-agi/nex-n2.5-mini:free",  # or "openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet"
        "BASE_URL": "https://openrouter.ai/api/v1",
        "API_KEY": os.getenv("LLM_API_KEY"),
    },
}
```

---

## Customizing Prompts & Fallbacks

You can customize the instructions given to the LLM and the message returned when no suitable answer is found:

```python title="settings.py"
RAGKIT = {
    # ...
    "LLM": {
        "PROVIDER": "openrouter",
        "MODEL": "nex-agi/nex-n2.5-mini:free",
        "BASE_URL": "https://openrouter.ai/api/v1",
        "API_KEY": os.getenv("LLM_API_KEY"),
        "OPTIONS": {
            "BASE_PROMPT": (
                "You are an assistant for Acme Corp. "
                "Answer the customer's question clearly and politely using only the provided facts. "
                "Do not make up facts."
            ),
            "NOT_FOUND_PROMPT": (
                "I'm sorry, but our documentation does not contain that information. "
                "Please reach out to support@acme.example.com."
            ),
        },
    },
}
```
