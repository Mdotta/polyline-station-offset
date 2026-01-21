FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt pyproject.toml ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

CMD ["pytest", "-q"]
