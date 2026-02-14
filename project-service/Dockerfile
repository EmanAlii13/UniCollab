# =========================
# Base image
# =========================
FROM python:3.12-slim

# =========================
# Prevent python from writing pyc files
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# Set working directory
# =========================
WORKDIR /app

# =========================
# Install system dependencies (for bcrypt etc.)
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Install Poetry
# =========================
RUN pip install --upgrade pip && \
    pip install poetry

# =========================
# Copy pyproject.toml and poetry.lock first
# =========================
COPY pyproject.toml poetry.lock* /app/

# =========================
# Install python dependencies (main only, no root project)
# =========================
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

# =========================
# Copy project files
# =========================
COPY . .

# =========================
# Expose internal container port
# =========================
EXPOSE 8000

# =========================
# Run app
# =========================
CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"]

