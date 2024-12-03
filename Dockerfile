FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction

COPY . /app

EXPOSE 5000

CMD ["sh", "-c", "poetry run flask db upgrade && poetry run python -m run"]
