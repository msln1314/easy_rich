# Build stage
FROM python:3.11-slim AS builder

# Set environment variables for better Python and Poetry behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies required by some packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装指定版本的 Poetry
RUN pip install poetry==${POETRY_VERSION}

# Set working directory and copy all files
WORKDIR /app
COPY . .

# Install dependencies and build wheel
RUN poetry install --only main --no-root --no-interaction && \
    poetry build --format=wheel && \
    pip install --no-cache-dir dist/*.whl

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy site-packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app/app /app/app
COPY --from=builder /app/run.py /app/run.py

# Set environment variables
ENV PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1 \
    PORT=8008

# Expose port
EXPOSE 8008

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8008/health || exit 1

# Set the default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"] 