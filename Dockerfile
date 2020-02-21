FROM python:3.8.1-slim-buster
LABEL maintainer="PSO SEAK"

# Base setup
WORKDIR /app
COPY requirements.txt .

#RUN apk --update add --no-cache g++ \
#    && apk add libpq postgresql-dev \
#    && apk add build-base

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV SRC_HOSTNAME="" \
    SRC_DB="" \
    SRC_ID="" \
    SRC_PASSWORD="" \
    DEST_HOSTNAME="" \
    DEST_PORT="" \
    DEST_DB="" \
    DEST_ID="" \
    DEST_PASSWORD=""

CMD ["python", "/app/main.py"]

