# =========================
# Base image
# =========================
FROM python:3.11-slim

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
# Install python dependencies
# =========================
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# Copy project files
# =========================
COPY . .

# =========================
# Expose internal container port
# =========================
EXPOSE 8001

# =========================
# Run app
# =========================
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
