# Settings Reference

All configuration for Django RAGKit lives inside the `RAGKIT` dictionary in your Django project's `settings.py`.

---

## Standard Configuration Example

This is the standard, minimal configuration required to run Django RAGKit:

```python title="settings.py"
import os

RAGKIT = {
    # Embedding provider configuration
    "EMBEDDING": {
        "PROVIDER": "openrouter",              # "openrouter" or "ollama"
        "MODEL": "baai/bge-m3",                # Model name
        "BASE_URL": "https://openrouter.ai/api/v1",  # Endpoint URL
        "DIMENSION": 1024,                     # Vector dimensions (<= 2000 for HNSW)
        "API_KEY": os.getenv("EMBEDDING_API_KEY"),
    },

    # Large Language Model (LLM) configuration
    "LLM": {
        "PROVIDER": "openrouter",              # "openrouter" or "ollama"
        "MODEL": "nex-agi/nex-n2.5-mini:free", # Model name
        "BASE_URL": "https://openrouter.ai/api/v1",
        "API_KEY": os.getenv("LLM_API_KEY"),
    },
}
```

---

## `EMBEDDING`

Configures the provider responsible for vectorizing questions and queries.

| Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `PROVIDER` | `str` | Yes | Name of the embedding provider (`"openrouter"` or `"ollama"`). |
| `MODEL` | `str` | Yes | Identifier of the embedding model (e.g., `baai/bge-m3`, `nomic-embed-text`). |
| `BASE_URL` | `str` | Yes | Base URL of the API endpoint. |
| `DIMENSION` | `int` | Yes | Dimensionality of the generated vector (e.g. `1024`, `768`, `1536`). You must obtain this exact value from your chosen embedding model's specifications. Note that the maximum supported dimension is **2000** (`max = 2000`) due to pgvector indexing constraints. |
| `API_KEY` | `str` | Optional | API token for authenticated services (e.g. OpenRouter). |

> [!WARNING]
> **Vector Dimension Limits**: pgvector supports indexing vectors up to **2000 dimensions** with HNSW. If your model produces vectors larger than 2000 dimensions, PostgreSQL will reject index creation.
> 
> **Crucial**: If you change `DIMENSION` **or switch to a different embedding model** (even if the new model uses the exact same vector dimension), you **must run** `python manage.py reset_embeddings`. Different models map text into completely different, incompatible latent semantic spaces—vectors from one model cannot be compared against vectors from another. See [Reset Embeddings](../operations/reset-embeddings.md).

---

## `LLM`

Configures the generative model responsible for formulating natural-language answers based on retrieved context.

| Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `PROVIDER` | `str` | Yes | Name of the LLM provider (`"openrouter"` or `"ollama"`). |
| `MODEL` | `str` | Yes | Model identifier (e.g., `llama3.2`, `nex-agi/nex-n2.5-mini:free`). |
| `BASE_URL` | `str` | Yes | Base URL of the inference endpoint. |
| `API_KEY` | `str` | Optional | API token for authenticated services (e.g. OpenRouter). |

---

## Optional & Advanced Configurations

The following settings are optional and allow you to enforce user authentication or customize prompt behaviors.

### 1. `BASE_SETTING` (Authentication Control)

By default, Django RAGKit allows guest visitors to use the chat interface. You can enforce mandatory user login by adding `BASE_SETTING`:

```python title="settings.py"
RAGKIT = {
    # ... EMBEDDING and LLM settings ...

    # Optional: Enforce authentication
    "BASE_SETTING": {
        "LOGIN_REQUIRED": True,  # Default is False
    },
}
```

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `LOGIN_REQUIRED` | `bool` | `False` | When `True`, unauthenticated users cannot access chat views or submit messages. HTML views redirect to login, and API endpoints return HTTP 401. |

---

### 2. `LLM.OPTIONS` (Custom Prompts & Fallback Message)

You can customize the instructions provided to the LLM or define a custom response message when no suitable knowledge match is found:

```python title="settings.py"
RAGKIT = {
    "LLM": {
        "PROVIDER": "openrouter",
        "MODEL": "nex-agi/nex-n2.5-mini:free",
        "BASE_URL": "https://openrouter.ai/api/v1",
        "API_KEY": os.getenv("LLM_API_KEY"),

        # Optional prompt customizations
        "OPTIONS": {
            "BASE_PROMPT": (
                "You are an expert customer service assistant. "
                "Answer questions strictly based on the provided dataset."
            ),
            "NOT_FOUND_PROMPT": (
                "I apologize, but I could not find information about your question in our database. "
                "Please reach out to support@example.com."
            ),
        },
    },
    # ... EMBEDDING settings ...
}
```

#### `BASE_PROMPT`
Overrides the default system prompt sent to the LLM during RAG generation.

**Default prompt:**
```text
You are a friendly and helpful assistant.
Answer the user's questions based on the provided context.
Use a natural, conversational tone, as if you're talking to a friend.
Keep your answers clear, concise, and easy to understand.
If the answer is not available in the provided context, say so honestly.
Respond using the same language as `user_question`.
```

#### `NOT_FOUND_PROMPT`
The canned response returned immediately when:
1. No similar questions exist in the database, or
2. The highest similarity percentage is **below 50%**.

**Default fallback response:**
```text
Sorry, I couldn't find information about that. Please contact support for assistance.
```
