# Python Package (pip)

This guide covers installing and configuring **Django RAGKit** as a Python package inside an existing Django project using `pip`.

---

## Requirements

Before installing Django RAGKit, ensure your environment meets the following specifications:

- **Python**: `3+`
- **Django**: `5.0+`
- **Database**: PostgreSQL 13+  

---

## 1. Install With pip

Install Django RAGKit using `pip`. All required core dependencies (`pgvector`, `psycopg2-binary`, and `requests`) are bundled and installed automatically:

```bash
pip install django-ragkit
```

---

## 2. Add to `INSTALLED_APPS`

Add `django.contrib.postgres` and `django_ragkit` to your `INSTALLED_APPS` in `settings.py`:

```python title="settings.py"
INSTALLED_APPS = [
    # Django core apps...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Add these 2 packages
    "django.contrib.postgres",  # PostgreSQL support (Required for vector fields & search)
    "django_ragkit",  # Django RAGKit
]
```

---

## 3. Apply Migrations

Run database migrations to enable pgvector, create the required tables, and build vector indexes:

```bash
python manage.py migrate
```

> [!TIP]
> **Automatic pgvector Extension**:
> You do **not** need to enable the `vector` extension manually in PostgreSQL. Django RAGKit's initial migration (`0001_initial.py`) executes `VectorExtension()`, which automatically runs `CREATE EXTENSION IF NOT EXISTS vector;` during `migrate`.

This command sets up the following tables:
- `django_ragkit_questionanswer`
- `django_ragkit_qaembedding` (with HNSW vector index)
- `django_ragkit_chat`
- `django_ragkit_askedquestion`
- `django_ragkit_generatedanswer`

---

## 4. Configure `RAGKIT` Settings

Define the `RAGKIT` dictionary in `settings.py`:

```python title="settings.py"
import os

RAGKIT = {
    "BASE_SETTING": {
        "LOGIN_REQUIRED": False,  # Optional: Set True to require authentication
    },
    "EMBEDDING": {
        "PROVIDER": "openrouter",  # "openrouter" or "ollama"
        "MODEL": "baai/bge-m3",
        "BASE_URL": "https://openrouter.ai/api/v1",
        "DIMENSION": 1024,  # max 2000
        "API_KEY": os.getenv("EMBEDDING_API_KEY"),
    },
    "LLM": {
        "PROVIDER": "openrouter",  # "openrouter" or "ollama"
        "MODEL": "nex-agi/nex-n2.5-mini:free",
        "BASE_URL": "https://openrouter.ai/api/v1",
        "API_KEY": os.getenv("LLM_API_KEY"),
    },
}
```

> [!IMPORTANT]
> **Default Database Vector Dimension (1024)**:
> The database schema and pre-packaged migrations in Django RAGKit default to **1024 dimensions** (matched with models such as `baai/bge-m3`).
> 
> If you want to use an embedding model with a different dimension (e.g. `768`, `1536` — up to `2000`), update `"DIMENSION"` in your `settings.py` and run the command:
> ```bash
> python manage.py reset_embeddings
> ```
> This command updates the vector column dimension, rebuilds the HNSW index, and creates the migration automatically. See the [Reset Embeddings](../operations/reset-embeddings.md) guide for details.

---

## 5. Include URL Routing

Include `django_ragkit.urls` in your project's root `urls.py`:

```python title="urls.py"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_ragkit.urls")),  # Mounts /chat/, /chat/<uuid>/, etc.
]
```

---

## Next Steps

Now that installation is complete, proceed to [Settings Reference](../configuration/settings.md) or explore the [Chat Interface](../ui/chat-interface.md) to integrate the chat component into your frontend!
