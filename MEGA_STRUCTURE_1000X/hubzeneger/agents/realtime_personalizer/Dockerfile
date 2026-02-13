FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared & base
COPY agents/base_agent.py /app/agents/base_agent.py
COPY shared /app/shared

# Copy this agent
COPY agents/realtime_personalizer /app/agents/realtime_personalizer

ENV PYTHONPATH=/app

CMD ["python", "agents/realtime_personalizer/agent.py"]