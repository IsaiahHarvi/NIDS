ARG REGISTRY
FROM ${REGISTRY}/torch-base
LABEL org.opencontainers.image.source https://github.com/isaiahharvi/nids

COPY deploy/offline_feeder/requirements.txt /app/requirements.txt
RUN uv pip install --system --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

COPY data/flows/test_data_small.csv /app/data/flows/test_data_small.csv
COPY src/grpc_ /app/src/grpc_
COPY src/ai/ /app/src/ai
COPY src/services/offline_feeder/offline_feeder.py /app/main.py

ENV PORT=50054
ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["uv", "run", "main.py"]
