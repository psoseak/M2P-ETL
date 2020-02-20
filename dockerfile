FROM python:3.8.1-alpine
LABEL maintainer="PSO SEAK"

# Base setup
WORKDIR /app
COPY . /app
RUN pip3 install -r /app/requirements.txt

ENV SRC_HOSTNAME="" \
    SRC_DB="" \
    SRC_ID="" \
    SRC_PASSWORD="" \
    DEST_HOSTNAME="" \
    DEST_DB="" \
    DEST_ID="" \
    DEST_PASSWORD=""

CMD ["python3", "/app/main.py"]

