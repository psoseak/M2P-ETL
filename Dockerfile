FROM python:3.8.2-slim
LABEL maintainer="PSO SEAK"

# Base setup
WORKDIR /app
COPY . /app
RUN \
    # Update OS
    apt-get -y update && \
    apt-get -y upgrade && \
    \
    # Install python dependencies
    pip3 install --no-cache-dir -r /app/requirements.txt

ENV SRC_HOSTNAME="" \
    SRC_PORT="" \
    SRC_DB="" \
    SRC_ID="" \
    SRC_PASSWORD="" \
    DEST_HOSTNAME="" \
    DEST_PORT="" \
    DEST_DB="" \
    DEST_ID="" \
    DEST_PASSWORD=""

CMD ["python3", "/app/main.py"]
