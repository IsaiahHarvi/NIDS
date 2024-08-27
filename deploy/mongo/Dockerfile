# mongo-client service
FROM python:3.11-slim

RUN pip install --no-cache-dir pymongo icecream

COPY src/services/mongo/mongo.py /app/main.py

WORKDIR /app

CMD ["python", "main.py"]
