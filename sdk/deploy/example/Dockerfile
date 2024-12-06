FROM python:3.11-slim

ENV PORT=50070
ENV arg1="Hello World"

COPY sdk/deploy/example/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

COPY src/grpc_ /app/src/grpc_
COPY sdk/services/example/main.py /app/main.py

ENV PYTHONPATH=/app/src
WORKDIR /app

CMD ["python", "main.py"]
