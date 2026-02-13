FROM python:3.11-slim
WORKDIR /app
COPY agents/surveyor/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY agents/surveyor /app/agents/surveyor
ENV PYTHONPATH=/app
CMD ["python", "agents/surveyor/surveyor.py"]
