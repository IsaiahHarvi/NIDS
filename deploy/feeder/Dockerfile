FROM python:3.11-slim

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --fix-missing -y tshark \
    libusb-1.0-0-dev libdbus-glib-1-dev libbluetooth-dev libnl-genl-3-dev

ENV PORT=50053
ENV INTERFACE="eth0"
ENV FILE_NAME="capture.pcap"
ENV DURATION=10

LABEL ENV_VARS="INTERFACE,FILE_NAME,DURATION"

COPY deploy/feeder/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/services/feeder/feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python", "main.py"]
