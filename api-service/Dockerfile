FROM python:3.13-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY app/ ./app/
COPY tests/ ./tests/
COPY .coveragerc ./
COPY models/ ./models/
COPY --chmod=755 entrypoint.sh /entrypoint.sh

ENV PYTHONPATH=/app

RUN /entrypoint.sh test

ENTRYPOINT ["/entrypoint.sh"]
CMD ["test"]

FROM base AS production

COPY app/ ./app/
COPY models/ ./models/
COPY --chmod=755 entrypoint.sh /entrypoint.sh

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["runserver"]

