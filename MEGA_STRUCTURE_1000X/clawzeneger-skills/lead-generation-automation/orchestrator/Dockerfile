FROM python:3.11-slim
WORKDIR /app
COPY orchestrator/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY orchestrator /app/orchestrator
ENV PYTHONPATH=/app
CMD ["python", "orchestrator/orchestrator.py"]
