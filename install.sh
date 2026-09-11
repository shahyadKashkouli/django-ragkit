#!/bin/bash

set -e

PROJECT_DIR="/opt/django-ragkit"
BASE_URL="https://raw.githubusercontent.com/shahyadKashkouli/django-ragkit/main"

echo "========================================"
echo "       Django RAGKit Installation"
echo "========================================"
echo

echo "Creating project directory..."

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "Downloading Docker Compose configuration..."

curl -fsSL -o compose.yml \
    "$BASE_URL/compose.yml"

echo "Downloading Docker environment configuration..."

curl -fsSL -o .env.docker \
    "$BASE_URL/.env.docker"

echo "Downloading environment template..."

curl -fsSL -o .env \
    "$BASE_URL/.env.example"

echo
echo "========================================"
echo "       Django RAGKit Configuration"
echo "========================================"
echo

echo "Configure Django and database settings."
echo "Press Enter to use the default value shown in brackets."
echo

read -rp "PostgreSQL database name [dockerdjango]: " POSTGRES_DB </dev/tty
POSTGRES_DB=${POSTGRES_DB:-dockerdjango}

echo

read -rp "PostgreSQL username [dbuser]: " POSTGRES_USER </dev/tty
POSTGRES_USER=${POSTGRES_USER:-dbuser}

echo

read -rsp "PostgreSQL password: " POSTGRES_PASSWORD </dev/tty
echo

echo

read -rp "Enable Django DEBUG mode?(default True): " DEBUG </dev/tty
DEBUG=${DEBUG:-True}

echo

echo "Django allowed hosts:"
echo "  localhost and 127.0.0.1 are always included."
echo "  You can optionally add extra hosts or domain names."
echo

read -rp "Additional allowed hosts (optional): " EXTRA_ALLOWED_HOSTS </dev/tty

DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"

if [ -n "$EXTRA_ALLOWED_HOSTS" ]; then
    EXTRA_ALLOWED_HOSTS=$(echo "$EXTRA_ALLOWED_HOSTS" | tr -d ' ')
    DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS},${EXTRA_ALLOWED_HOSTS}"
fi

echo

read -rsp "Embedding API key: " EMBEDDING_API_KEY </dev/tty
echo

echo

read -rsp "LLM API key: " LLM_API_KEY </dev/tty
echo

echo
echo "Generating Django secret key..."

DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

echo "Updating environment configuration..."

sed -i "s|^DJANGO_SECRET_KEY=.*|DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}|" .env
sed -i "s|^DEBUG=.*|DEBUG=${DEBUG}|" .env
sed -i "s|^DJANGO_ALLOWED_HOSTS=.*|DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}|" .env
sed -i "s|^POSTGRES_DB=.*|POSTGRES_DB=${POSTGRES_DB}|" .env
sed -i "s|^POSTGRES_USER=.*|POSTGRES_USER=${POSTGRES_USER}|" .env
sed -i "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=${POSTGRES_PASSWORD}|" .env
sed -i "s|^EMBEDDING_API_KEY=.*|EMBEDDING_API_KEY=${EMBEDDING_API_KEY}|" .env
sed -i "s|^RAGKIT_EMBEDDING_API_KEY=.*|RAGKIT_EMBEDDING_API_KEY=${EMBEDDING_API_KEY}|" .env
sed -i "s|^LLM_API_KEY=.*|LLM_API_KEY=${LLM_API_KEY}|" .env
sed -i "s|^RAGKIT_LLM_API_KEY=.*|RAGKIT_LLM_API_KEY=${LLM_API_KEY}|" .env

echo
echo "Configuration completed successfully."

echo "========================================"
echo "       Starting Django RAGKit"
echo "========================================"
echo

docker compose up -d
echo
docker compose exec -T ragkit python manage.py migrate </dev/null
echo Database migrations completed successfully.


echo
echo "------------------------------------------------------------"
echo "Optional - Create Django Admin User"
echo "------------------------------------------------------------"
echo
echo "You can optionally create a Django superuser."
echo "Press Enter without entering a username to skip this step."
echo

printf "Superuser username (optional): " > /dev/tty
read SUPERUSER_USERNAME < /dev/tty

if [ -z "$SUPERUSER_USERNAME" ]; then
    echo
    echo "Skipping superuser creation."
else
    echo
    echo "Starting Django superuser creation..."
    echo

    docker compose exec -it ragkit python manage.py createsuperuser \
        --username "$SUPERUSER_USERNAME" </dev/tty
fi



echo
echo "========================================"
echo "       Installation Complete"
echo "========================================"
echo
echo "Django RAGKit has been started successfully."
echo
echo "Project directory:"
echo "  $(pwd)"
echo
echo "Open Django RAGKit at:"
echo "  http://localhost:8000"
echo
echo "To view container status:"
echo "  cd $(pwd)"
echo "  docker compose ps"
echo
echo "To view logs:"
echo "  cd $(pwd)"
echo "  docker compose logs -f"
echo