FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=never \
  UV_PROJECT_ENVIRONMENT=/app/.venv

RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional

COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

# for efficiency
COPY pyproject.toml uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache \
  cd /_lock && \
  uv sync \
  --frozen \
  --no-install-project

COPY scripts/ ./scripts/
RUN sed -i "s/\r$//g" /app/scripts/entrypoint.dev.sh
RUN chmod +x /app/scripts/entrypoint.dev.sh

COPY . .

ENTRYPOINT ["/app/scripts/entrypoint.dev.sh"]
