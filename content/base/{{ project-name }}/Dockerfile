# The builder image, used to build the virtual environment
FROM --platform=linux/amd64 python:3.11-buster as builder

RUN pip install poetry

EXPOSE {{ chatbot-port }}
HEALTHCHECK CMD curl --fail http://localhost:{{ chatbot-port }}/_stcore/health

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM --platform=linux/amd64 python:3.11-slim-buster as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY logging.yaml ./
COPY ai_agent ./ai_agent

ENTRYPOINT ["python", "-m", "ai_agent.main"]