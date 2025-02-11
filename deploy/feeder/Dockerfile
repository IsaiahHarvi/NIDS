# Stage 1
FROM python:3.11-slim AS nfstream-builder

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    libpcap-dev \
    python3-dev \
    autoconf \
    automake \
    libtool \
    pkg-config \
    flex \
    bison \
    gettext \
    libjson-c-dev \
    libusb-1.0-0-dev \
    libdbus-glib-1-dev \
    libbluetooth-dev \
    libnl-genl-3-dev \
    git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /nfstream
RUN git clone --recurse-submodules git+https://github.com/praetoriannero/nfstream.git .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r dev_requirements.txt
RUN python3 -m pip install --prefix=/nfstream-install .

# Stage 2
FROM torch-base

COPY --from=nfstream-builder /nfstream-install /usr/local

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libpcap-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY deploy/feeder/requirements.txt /app/requirements.txt
RUN uv pip install --system --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

ENV PORT=50053
ENV INTERFACE="eth0"
ENV FILE_NAME="capture.pcap"
ENV DURATION=5
LABEL ENV_VARS="INTERFACE,FILE_NAME,DURATION"

COPY src/grpc_ /app/src/grpc_
COPY src/services/feeder/feeder.py /app/main.py
COPY src/ai/BasicModule.py /app/src/ai/BasicModule.py
COPY data/checkpoints/MLP.ckpt /app/model.ckpt

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["uv", "run", "main.py"]
