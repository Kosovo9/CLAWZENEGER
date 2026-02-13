FROM python:3.11-slim

WORKDIR /app

COPY agents/coder_10000x/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared & base
COPY agents/base_agent.py /app/agents/base_agent.py
COPY shared /app/shared

# Copy this agent
COPY agents/coder_10000x /app/agents/coder_10000x

ENV PYTHONPATH=/app

CMD ["python", "agents/coder_10000x/agent.py"]