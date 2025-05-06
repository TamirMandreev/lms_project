FROM python:3.12-slim

WORKDIR /app
COPY . /app/

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 8000

CMD python3 manage.py migrate \
    && python3 manage.py runserver 0.0.0.0:8000
