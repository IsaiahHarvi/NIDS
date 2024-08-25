FROM python:3.11-slim

ARG PORT
ENV PORT=${PORT}

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY deploy/model/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt --retries 1 && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/ai/BasicModule.py /app/src/ai/BasicModule.py

ARG MODEL_PATH
ARG FILE_NAME
COPY $MODEL_PATH /app/${MODEL_PATH}
COPY src/services/model/${FILE_NAME} /app/main.py

CMD ["python", "main.py"]