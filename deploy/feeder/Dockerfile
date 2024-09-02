FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    jnetpcap \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    openjdk-8-jdk \
    tshark \
    maven \
    gradle \
    git \
    wget \
    unzip \
    tar && \
    apt-get clean

# Create symbolic links to make Python 3.11 the default python3 and pip3
RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/bin/pip3 /usr/bin/pip
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Download jnetpcap
WORKDIR /app
RUN wget https://sourceforge.net/projects/jnetpcap/files/jnetpcap/1.4/jnetpcap-1.4.r1300-1.linux.x86_64.tgz/download -O jnetpcap-linux.tgz && \
    tar -xzf jnetpcap-linux.tgz && \
    cp $(find . -name "jnetpcap.jar") /app/jnetpcap.jar

# Install the jnetpcap JAR into the local Maven repo
RUN mvn install:install-file \
    -Dfile=/app/jnetpcap.jar \
    -DgroupId=org.jnetpcap \
    -DartifactId=jnetpcap \
    -Dversion=1.4.1 \
    -Dpackaging=jar

# Set up CICFlowMeter
RUN git clone https://github.com/ahlashkari/CICFlowMeter.git /app/repo && ls -l /app/repo 
WORKDIR /app/repo
RUN chmod +x ./gradlew
RUN ./gradlew distZip --stacktrace --debug
RUN unzip /app/repo/build/distributions/CICFlowMeter-4.0.zip -d /app/CICFlowMeter/ || true
RUN chmod +x /app/CICFlowMeter/CICFlowMeter-4.0/bin/CICFlowMeter

# Set up gRPC and start the feeder
ENV PORT=50053
ENV INTERFACE="eth0"
ENV FILE_NAME="capture.pcap"
ENV DURATION=10
ENV HOST="neural-network"
ENV TARGET_PORT=50052

LABEL ENV_VARS="INTERFACE,FILE_NAME,DURATION,HOST,TARGET_PORT"

COPY deploy/feeder/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt --retries 3 && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/services/feeder/feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python3", "main.py"]
