FROM python:3.8.1-slim
LABEL maintainer="PSO SEAK"

# Base setup
WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r /app/requirements.txt

ENV SRC_HOSTNAME="" \
    SRC_DB="" \
    SRC_ID="" \
    SRC_PASSWORD="" \
    DEST_HOSTNAME="" \
    DEST_PORT="" \
    DEST_DB="" \
    DEST_ID="" \
    DEST_PASSWORD=""

CMD ["python3", "/app/main.py"]

