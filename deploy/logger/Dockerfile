FROM python:3.11-slim

ENV PORT=50055

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY deploy/logger/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt 

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY src/grpc_ /app/src/grpc_
COPY src/services/logger/compose_logger.py /app/main.py

CMD ["python", "main.py"]
