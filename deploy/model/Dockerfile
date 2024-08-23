FROM base-python:latest

COPY src/services/model/recurrent.py /app/recurrent.py
COPY data/checkpoints/RNN.ckpt data/checkpoints/RNN.ckpt

EXPOSE 50051

CMD ["python", "recurrent.py"]
