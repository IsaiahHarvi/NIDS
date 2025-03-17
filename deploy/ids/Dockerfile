ARG REGISTRY
FROM ${REGISTRY}/torch-base
LABEL org.opencontainers.image.source https://github.com/isaiahharvi/nids

WORKDIR /app

COPY src/grpc_ /app/src/grpc_
COPY src/ai/BasicModule.py /app/src/ai/BasicModule.py
COPY src/services/ids/ids.py /app/main.py

ARG MODEL_PATH
COPY $MODEL_PATH /app/model.ckpt

ENV PORT=50052
ENV PYTHONPATH=/app/src

CMD ["uv", "run", "main.py"]
