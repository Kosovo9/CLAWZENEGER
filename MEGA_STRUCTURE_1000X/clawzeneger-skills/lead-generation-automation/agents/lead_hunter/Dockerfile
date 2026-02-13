FROM python:3.11-slim
WORKDIR /app
COPY agents/lead_hunter/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY agents/lead_hunter /app/agents/lead_hunter
ENV PYTHONPATH=/app
CMD ["python", "agents/lead_hunter/hunter.py"]
