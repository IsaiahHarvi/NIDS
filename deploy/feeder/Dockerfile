FROM python:3.11-slim

ENV PORT=50053

ENV INTERFACE="eth0"
ENV FILE_NAME="capture.pcap"
ENV DURATION=10
# HOST is the name of the service that will be used to connect to the target service
ENV HOST="localhost"
ENV TARGET_PORT=50052

LABEL ENV_VARS="INTERFACE,FILE_NAME,DURATION,HOST,TARGET_PORT"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tshark argus-client argus-server && \
    apt-get clean

COPY deploy/feeder/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt --retries 1 && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/services/feeder/feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python", "main.py"]
