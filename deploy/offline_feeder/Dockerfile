FROM torch-base

ENV PORT=50054

COPY deploy/offline_feeder/requirements.txt /app/requirements.txt
RUN uv pip install --system --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

COPY data/CIC/test_data.csv /app/data/CIC/test_data.csv
COPY src/grpc_ /app/src/grpc_
COPY src/ai/ /app/src/ai
COPY src/services/offline_feeder/offline_feeder.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["uv", "run", "main.py"]
