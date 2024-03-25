FROM python:3.10-slim
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY . /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
