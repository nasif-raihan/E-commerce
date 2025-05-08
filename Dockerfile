FROM python:3.12-slim-bullseye as requirements

WORKDIR /app
RUN pip3 install -U pip && pip3 install poetry==1.8.3
COPY pyproject.toml poetry.lock ./
RUN poetry export --only main --format requirements.txt --output requirements.txt


FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /web

RUN apt update && apt install -y --no-install-recommends \
    build-essential gcc libpq-dev \
 && apt clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip
COPY --from=requirements /app/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "project.wsgi:application"]
