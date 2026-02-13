FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared & base
COPY agents/base_agent.py /app/agents/base_agent.py
COPY shared /app/shared

# Copy this agent
COPY agents/b2a2c_platform /app/agents/b2a2c_platform

ENV PYTHONPATH=/app

CMD ["python", "agents/b2a2c_platform/agent.py"]