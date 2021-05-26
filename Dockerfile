# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY ./app /app

WORKDIR /app
