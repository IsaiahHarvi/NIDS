FROM python:3.11-slim

ENV PORT=50054

COPY deploy/offline_feeder/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt --retries 1 && rm /app/requirements.txt

COPY data/CIC/test_data.csv /app/data/CIC/test_data.csv
COPY src/grpc_ /app/src/grpc_
COPY src/services/offline_feeder/offline_feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python", "main.py"]
