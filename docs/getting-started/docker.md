# Docker Quickstart

Django RAGKit provides full Docker Compose support with pre-configured PostgreSQL (`pgvector`), an official pre-built container image, and an automated one-line installer.

---

## Quick Install (Automated Installer)

The fastest and easiest way to install and run Django RAGKit on Linux or macOS is using the official one-line interactive installer script.

### 1. Run the Installer

Run the following command in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/shahyadKashkouli/django-ragkit/main/install.sh | bash
```

The installer script (`install.sh`) automates the entire deployment process end-to-end:

1. **Creates Installation Directory**: Creates a dedicated project directory at `/opt/django-ragkit`.
2. **Downloads Configurations**: Automatically downloads the latest `compose.yml`, `.env.docker`, and `.env.example` directly from GitHub.
3. **Interactive Configuration Wizard**: Prompts you for your environment settings with sensible defaults:
    - PostgreSQL database name, user, and password
    - Django `DEBUG` mode toggle
    - Allowed hosts (with `localhost` and `127.0.0.1` included automatically)
    - Embedding provider API key
    - LLM provider API key
4. **Automatic Secret Key Generation**: Generates a cryptographically secure 50-character `DJANGO_SECRET_KEY` using Python's `secrets` module and writes all values to `.env`.
5. **Starts Docker Containers**: Executes `docker compose up -d` using the official pre-built image and PostgreSQL with `pgvector`.
6. **Applies Database Migrations**: Automatically runs `docker compose exec -T ragkit python manage.py migrate` to apply all migrations and activate the vector database extension.
7. **Creates Admin Superuser (Optional)**: Prompts you to optionally create a Django superuser interactively.
8. **Ready to Use**: Makes Django RAGKit immediately accessible at `http://localhost:8000`.

---

### 2. Configuring Django & RAGKit (`settings.py` via `.env`)

When running Django RAGKit in Docker, **you do not need to modify `settings.py` directly inside the container**. All application and pipeline configurations in `settings.py` are mapped to environment variables and managed entirely through the `.env` file located at `/opt/django-ragkit/.env`.

To configure or update your settings, open the file using `nano`:

```bash
nano /opt/django-ragkit/.env
```

#### Available Configuration Variables

Here are the primary variables and how they map to Django and the `RAGKIT` dictionary in `settings.py`:

| Variable | Maps to `settings.py` | Default / Description |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | `SECRET_KEY` | Cryptographic secret key for Django sessions and security |
| `DEBUG` | `DEBUG` | `True` for development, `False` for production |
| `DJANGO_ALLOWED_HOSTS` | `ALLOWED_HOSTS` | Comma-separated list of allowed domains/IPs (e.g. `localhost,127.0.0.1`) |
| `POSTGRES_DB` | `DATABASES['default']['NAME']` | PostgreSQL database name (e.g. `dockerdjango`) |
| `POSTGRES_USER` | `DATABASES['default']['USER']` | PostgreSQL database user (e.g. `dbuser`) |
| `POSTGRES_PASSWORD` | `DATABASES['default']['PASSWORD']` | PostgreSQL database password |
| `RAGKIT_LOGIN_REQUIRED` | `RAGKIT['BASE_SETTING']['LOGIN_REQUIRED']` | Set `True` to require user login for chat access |
| `RAGKIT_EMBEDDING_PROVIDER` | `RAGKIT['EMBEDDING']['PROVIDER']` | Embedding provider (`openrouter` or `ollama`) |
| `RAGKIT_EMBEDDING_MODEL` | `RAGKIT['EMBEDDING']['MODEL']` | Embedding model (e.g. `baai/bge-m3` or `nomic-embed-text`) |
| `RAGKIT_EMBEDDING_BASE_URL` | `RAGKIT['EMBEDDING']['BASE_URL']` | API endpoint (e.g. `https://openrouter.ai/api/v1`) |
| `RAGKIT_EMBEDDING_DIMENSION` | `RAGKIT['EMBEDDING']['DIMENSION']` | Vector dimension size (e.g. `1024` or `768`, max: 2000) |
| `RAGKIT_EMBEDDING_API_KEY` | `RAGKIT['EMBEDDING']['API_KEY']` | API key for embedding provider |
| `RAGKIT_LLM_PROVIDER` | `RAGKIT['LLM']['PROVIDER']` | LLM provider (`openrouter` or `ollama`) |
| `RAGKIT_LLM_MODEL` | `RAGKIT['LLM']['MODEL']` | LLM model name (e.g. `nex-agi/nex-n2.5-mini:free`) |
| `RAGKIT_LLM_BASE_URL` | `RAGKIT['LLM']['BASE_URL']` | LLM endpoint URL |
| `RAGKIT_LLM_API_KEY` | `RAGKIT['LLM']['API_KEY']` | API key for LLM provider |
| `RAGKIT_LLM_BASE_PROMPT` | `RAGKIT['LLM']['OPTIONS']['BASE_PROMPT']` | *(Optional)* Custom system prompt for RAG answers |
| `RAGKIT_LLM_NOT_FOUND_PROMPT` | `RAGKIT['LLM']['OPTIONS']['NOT_FOUND_PROMPT']` | *(Optional)* Fallback message when no matching context exists |

---

### 3. Applying Changes

Whenever you modify `/opt/django-ragkit/.env`, restart the Docker containers to apply the new configuration:

```bash
cd /opt/django-ragkit
docker compose up -d
```

> [!IMPORTANT]
> **Changing Vector Dimensions (`RAGKIT_EMBEDDING_DIMENSION != 1024`)**:
> The default PostgreSQL database schema is pre-configured for **1024 dimensions** (matching models like `baai/bge-m3`).
> 
> If you set a different dimension in `.env` (such as `768` for Ollama's `nomic-embed-text` or `1536` for OpenAI models), PostgreSQL column constraints require updating the embeddings table schema.
> 
> You **must** run the `reset_embeddings` command inside the running Docker container:
> ```bash
> cd /opt/django-ragkit
> docker compose exec -T ragkit python manage.py reset_embeddings
> ```
> This command will:
> 
> 1. Safely archive your existing embeddings table into a backup table (zero data loss).
> 2. Rebuild the vector table with your new dimension and recreate the HNSW vector index.
> 3. Automatically synchronize Django migrations.
> 
> For full technical details and recovery options, see the [Reset Embeddings Command](../operations/reset-embeddings.md) guide.

---

> [!TIP]
> **Manual Docker Compose & Advanced Setup**:
> If you prefer deploying manually with Docker Compose, running custom images, connecting to local Ollama, or managing container lifecycles, see the comprehensive [Docker Image & Manual Setup](docker-image.md) guide.

