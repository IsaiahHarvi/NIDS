FROM python:3.11-slim

COPY .devcontainer/requirements-cpu.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && rm /app/requirements.txt

ARG MODEL_PATH
ARG FILE_NAME

COPY $MODEL_PATH /app/${MODEL_PATH}

# in the future, we need to avoid copying the whole src folder lol
COPY src/ /app/src
COPY src/services/model/${FILE_NAME} /app/main.py

WORKDIR /app

ENV PYTHONPATH=/app/src

CMD ["python", "main.py"]