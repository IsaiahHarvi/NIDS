FROM python:3.11-slim

ENV PORT=50055

COPY deploy/logger/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt 

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY src/grpc_ /app/src/grpc_
COPY src/services/logger/compose_logger.py /app/main.py

CMD ["python", "main.py"]
