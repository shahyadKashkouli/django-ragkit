# Providers Overview

Django RAGKit features a modular provider architecture designed to decouple AI backend services from core business logic.

---

## Provider Types

1. **LLM Providers (`django_ragkit.providers.LLM`)**:
   Responsible for taking the assembled context and query and producing an informed answer.
   - [Ollama LLM Provider](llm.md#ollama-local-privacy-focused) (Local, zero-cost, private)
   - [OpenRouter LLM Provider](llm.md#openrouter-cloud-multi-model-api) (Cloud gateway to Claude, GPT-4, Llama 3, Gemini, Mistral)

2. **Embedding Providers (`django_ragkit.providers.embeddings`)**:
   Responsible for converting arbitrary text into fixed-dimension floating-point vector arrays.
   - [Ollama Embeddings](embeddings.md#ollama-embeddings-local) (e.g. `nomic-embed-text`, `bge-m3`)
   - [OpenRouter Embeddings](embeddings.md#openrouter-embeddings-cloud) (e.g. `baai/bge-m3`, `openai/text-embedding-3-small`)

---

## Factory Pattern

Providers are instantiated on-demand using factory functions based on your `settings.RAGKIT` configuration:

```python
# Returns an instance of the configured LLM provider
from django_ragkit.providers.LLM.factory import get_LLM_provider
llm = get_LLM_provider()
answer = llm.generate_response(prompt)

# Returns an instance of the configured Embedding provider
from django_ragkit.providers.embeddings.factory import get_embedding_provider
embedder = get_embedding_provider()
vector = embedder.embed("How do I reset my password?")
```
