FROM python:3.8.1-alpine
LABEL maintainer="PSO SEAK"

# Base setup
WORKDIR /app
COPY . /app

RUN apk --update add --no-cache g++ \
    && apk add libpq postgresql-dev \
    && apk add build-base

RUN pip install --no-binary :all: -r /app/requirements.txt

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

