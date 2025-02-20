ARG REGISTRY
FROM ${REGISTRY}/python-base
LABEL org.opencontainers.image.source https://github.com/isaiahharvi/nids

COPY deploy/logger/requirements.txt /app/requirements.txt
RUN uv pip install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

WORKDIR /app
COPY src/grpc_ /app/src/grpc_
COPY src/services/logger/compose_logger.py /app/main.py

ENV PYTHONPATH=/app/src
ENV PORT=50055

CMD ["uv", "run", "main.py"]
