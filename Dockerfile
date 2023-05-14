FROM python:3.11-slim as builder

RUN pip install poetry
RUN mkdir -p /app
COPY . /app

WORKDIR /app

RUN poetry install --without dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "boteco/main.py"]
