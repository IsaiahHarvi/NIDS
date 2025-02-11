FROM torch-base

ENV PORT=50052

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY src/grpc_ /app/src/grpc_
COPY src/ai/BasicModule.py /app/src/ai/BasicModule.py

ARG MODEL_PATH
COPY $MODEL_PATH /app/model.ckpt
COPY src/services/neural_network/neural_network.py /app/main.py

CMD ["uv", "run", "main.py"]
