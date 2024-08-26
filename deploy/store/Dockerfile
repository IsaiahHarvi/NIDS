FROM python:3.11-slim

ENV CSV_OUT_NAME="output.csv"
LABEL ENVS="CSV_OUT_NAME"

COPY deploy/store/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt 

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY src/grpc_ /app/src/grpc_

ARG PORT
ARG SERVICE_FILE_NAME
ENV PORT=${PORT}

COPY src/services/store/${SERVICE_FILE_NAME} /app/main.py

CMD ["python", "main.py"]
