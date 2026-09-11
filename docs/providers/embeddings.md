# Embedding Providers

Embedding providers convert human text into mathematical vectors, enabling semantic similarity matching through cosine distance in PostgreSQL pgvector.

---

## Ollama Embeddings (Local)

### 1. Pull the Model

Run Ollama and pull an embedding-specific model:

```bash
ollama pull nomic-embed-text
```

Popular embedding models on Ollama:
- `nomic-embed-text` (768 dimensions)
- `bge-m3` (1024 dimensions)
- `all-minilm` (384 dimensions)

### 2. Configuration in `settings.py`

```python title="settings.py"
RAGKIT = {
    # ...
    "EMBEDDING": {
        "PROVIDER": "ollama",
        "MODEL": "nomic-embed-text",
        "BASE_URL": "http://localhost:11434",
        "DIMENSION": 768,  # Must match the model's output dimensionality
    },
}
```

---

## OpenRouter Embeddings (Cloud)

### 1. Obtain an API Key

Generate an API key at [openrouter.ai](https://openrouter.ai/) and store it in `EMBEDDING_API_KEY`.

### 2. Configuration in `settings.py`

```python title="settings.py"
import os

RAGKIT = {
    # ...
    "EMBEDDING": {
        "PROVIDER": "openrouter",
        "MODEL": "baai/bge-m3",
        "BASE_URL": "https://openrouter.ai/api/v1",
        "DIMENSION": 1024,
        "API_KEY": os.getenv("EMBEDDING_API_KEY"),
    },
}
```

---

## Understanding Vector Dimensions & pgvector Constraints

Each embedding model outputs a vector with a fixed number of floating-point numbers (dimensions). For example:
- `baai/bge-m3`: 1024 dimensions
- `nomic-embed-text`: 768 dimensions
- `openai/text-embedding-3-small`: 1536 dimensions

> [!WARNING]
> **HNSW Index Limit (Max 2000 Dimensions)**:
> In PostgreSQL with pgvector, indexed columns using `HnswIndex` or `IvfflatIndex` cannot exceed **2000 dimensions**. Always ensure your chosen embedding model produces `<= 2000` dimensions.

> [!IMPORTANT]
> **Changing Models or Dimensions Requires Re-Indexing**:
> - **Dimension Changes**: PostgreSQL `vector(N)` strictly validates the dimension of each row, so changing dimensions requires rebuilding the database table schema.
> - **Model Changes**: Even if two models share the exact same dimension size (e.g. both are 1024), they map language into completely different, incompatible latent semantic spaces. Vectors produced by different models cannot be compared with cosine distance.
> 
> Whenever you change the embedding model or dimension, you **must run**:
> ```bash
> python manage.py reset_embeddings
> ```
> See the [Reset Embeddings](../operations/reset-embeddings.md) documentation for full instructions.
