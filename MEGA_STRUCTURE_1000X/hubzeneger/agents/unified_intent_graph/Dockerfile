FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared & base
COPY agents/base_agent.py /app/agents/base_agent.py
COPY shared /app/shared

# Copy this agent
COPY agents/unified_intent_graph /app/agents/unified_intent_graph

ENV PYTHONPATH=/app

CMD ["python", "agents/unified_intent_graph/agent.py"]