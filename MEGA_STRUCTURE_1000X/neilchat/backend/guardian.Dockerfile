FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir psutil requests docker

COPY app/workers/guardian.py .

CMD ["python", "guardian.py"]
