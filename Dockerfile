# Use official Python 3.12 slim image
FROM python:3.12-slim

# Avoid Python writing .pyc files and make output unbuffered for CI logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools (some deps may need compilation). Keep layer small.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first for Docker layer caching
# If you use pyproject.toml/poetry, adjust accordingly.
COPY requirements.txt /app/

# Install runtime and dev dependencies if files exist
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy the rest of the project
COPY . /app

# Make the package importable from /app/src
ENV PYTHONPATH=/app/src

# Default command is to run the test suite (evaluator can override)
CMD ["pytest", "-q"]
