FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared & base
COPY agents/base_agent.py /app/agents/base_agent.py
COPY shared /app/shared

# Copy this agent
COPY agents/causal_models /app/agents/causal_models

ENV PYTHONPATH=/app

CMD ["python", "agents/causal_models/agent.py"]