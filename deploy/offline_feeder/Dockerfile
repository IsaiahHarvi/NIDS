FROM python:3.11-slim

ENV PORT=50054

# HOST is the name of the service that will be used to connect to the target service
ENV P2P="true"
ENV HOST="residual"
ENV TARGET_PORT=50052

LABEL ENV_VARS="P2P,HOST,TARGET_PORT"

COPY deploy/model/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt --retries 1 && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/services/offline_feeder/offline_feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python", "main.py"]
