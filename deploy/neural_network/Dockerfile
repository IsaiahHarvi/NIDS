FROM python:3.11-slim

ENV PORT=50052

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY deploy/neural_network/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt --retries 3 && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY src/ai/BasicModule.py /app/src/ai/BasicModule.py

ARG MODEL_PATH
COPY $MODEL_PATH /app/model.ckpt
COPY src/services/neural_network/neural_network.py /app/main.py

CMD ["python", "main.py"]
