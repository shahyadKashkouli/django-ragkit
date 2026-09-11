# Docker Image & Manual Setup

This guide covers the official Django RAGKit Docker image, manual Docker Compose deployments, standalone container execution, and connecting to host services like local Ollama.

---

## Official Docker Hub Image

Django RAGKit provides an official, pre-built container image published on Docker Hub. This image allows you to run Django RAGKit instantly without installing Python or compiling dependencies locally.

### Pull the Image

To download the latest image:

```bash
docker pull shincuff/django-ragkit:latest
```

The repository is publicly accessible at [shincuff/django-ragkit](https://hub.docker.com/r/shincuff/django-ragkit).

### Key Highlights

- **Pre-packaged Dependencies**: Includes Python 3.13, Django 6, `pgvector`, `psycopg2-binary`, and all Django RAGKit components pre-installed.
- **Zero Compilation**: No need to install build essentials or compile C-extensions on your host system.
- **Production Ready**: Optimized container footprint with immediate readiness for PostgreSQL & pgvector integration.
- **Pre-configured Entrypoint**: Automatically runs the Django server on port `8000` via `manage.py runserver 0.0.0.0:8000`.

---

## Manual Docker Compose Setup

If you prefer to configure and run the stack manually instead of using the automated installer script, follow the steps below.

### 1. Docker Compose Configuration

Create a project directory and add the following `compose.yml` file:

```yaml title="compose.yml"
services:
  postgres:
    image: pgvector/pgvector:pg17
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env
      - .env.docker

  ragkit:
    image: shincuff/django-ragkit:latest
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    env_file:
      - .env
      - .env.docker
    extra_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  postgres_data:
```

> [!TIP]
> **Local Source Development**:
> If you are developing Django RAGKit itself and want live code reloading from your host machine, you can mount your local directory by adding `volumes: - .:/app` and replacing `image: shincuff/django-ragkit:latest` with `build: .`.

---

### 2. Environment Files

#### `.env` File

Create your primary `.env` file containing database credentials, security keys, and RAGKit provider settings:

```bash title=".env"
DJANGO_SECRET_KEY=your-secure-random-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=dockerdjango
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=your-database-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Require authentication for chat (optional)
# RAGKIT_LOGIN_REQUIRED=False

# Embedding Configuration
RAGKIT_EMBEDDING_PROVIDER=openrouter
RAGKIT_EMBEDDING_MODEL=baai/bge-m3
RAGKIT_EMBEDDING_BASE_URL=https://openrouter.ai/api/v1
RAGKIT_EMBEDDING_DIMENSION=1024
RAGKIT_EMBEDDING_API_KEY=your-embedding-api-key

# LLM Configuration
RAGKIT_LLM_PROVIDER=openrouter
RAGKIT_LLM_MODEL=nex-agi/nex-n2.5-mini:free
RAGKIT_LLM_BASE_URL=https://openrouter.ai/api/v1
RAGKIT_LLM_API_KEY=your-llm-api-key

# Custom Prompts (optional)
# RAGKIT_LLM_BASE_PROMPT=
# RAGKIT_LLM_NOT_FOUND_PROMPT=
```

#### `.env.docker` File

Create a `.env.docker` file to configure inter-container networking. This overrides `DATABASE_HOST` so the `ragkit` service communicates with the database container via its Docker network alias (`postgres`):

```bash title=".env.docker"
DATABASE_HOST=postgres
```

---

### 3. Starting the Services

Launch both PostgreSQL and the Django RAGKit service in detached mode:

```bash
docker compose up -d
```

---

### 4. Running Migrations in Docker

Once the containers are running, execute database migrations inside the `ragkit` container:

```bash
docker compose exec -T ragkit python manage.py migrate
```

Create an administrative superuser to access the Django admin panel:

```bash
docker compose exec -it ragkit python manage.py createsuperuser
```

> [!NOTE]
> **Custom Vector Dimension (`RAGKIT_EMBEDDING_DIMENSION != 1024`)**:
> If you specified a dimension other than `1024` in `.env`, update the vector schema by executing:
> ```bash
> docker compose exec -T ragkit python manage.py reset_embeddings
> ```

You can now access:
- **Chat Interface**: [http://localhost:8000/ai/chat/](http://localhost:8000/ai/chat/)
- **Admin Dashboard**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Standalone Container (`docker run`)

You can also run the pre-built image as a standalone container, pointing to an existing PostgreSQL database:

```bash
docker run -d \
  --name django-ragkit \
  -p 8000:8000 \
  --env-file .env \
  shincuff/django-ragkit:latest
```

---

## Connecting to Local Ollama from Docker

If you want to run Ollama locally on your host machine while Django runs inside the Docker container:

1. **Configure Ollama to listen on all network interfaces**:
   ```bash
   OLLAMA_HOST=0.0.0.0:11434 ollama serve
   ```

2. **Point `BASE_URL` to `host.docker.internal` in your `.env`**:
   ```bash title=".env"
   RAGKIT_EMBEDDING_PROVIDER=ollama
   RAGKIT_EMBEDDING_MODEL=nomic-embed-text
   RAGKIT_EMBEDDING_BASE_URL=http://host.docker.internal:11434
   RAGKIT_EMBEDDING_DIMENSION=768

   RAGKIT_LLM_PROVIDER=ollama
   RAGKIT_LLM_MODEL=llama3.2
   RAGKIT_LLM_BASE_URL=http://host.docker.internal:11434
   ```

> [!NOTE]
> The `extra_hosts: ["host.docker.internal:host-gateway"]` directive in `compose.yml` ensures that the `ragkit` container can resolve and communicate with services running on your host machine.

---

## Common Management Commands

Use these standard commands to manage your Docker Compose deployment:

| Action | Command |
| :--- | :--- |
| **Check container status** | `docker compose ps` |
| **View live logs** | `docker compose logs -f` |
| **View RAGKit application logs only** | `docker compose logs -f ragkit` |
| **Restart services** | `docker compose restart` |
| **Stop services** | `docker compose down` |
| **Stop services & delete database volume** | `docker compose down -v` |

---

## Building from Source

If you prefer building a custom Docker image from the local source repository:

```bash
docker build -t django-ragkit:latest .
```
