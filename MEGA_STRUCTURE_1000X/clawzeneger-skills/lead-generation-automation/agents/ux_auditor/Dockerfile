FROM python:3.11-slim
WORKDIR /app
COPY agents/ux_auditor/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY agents/ux_auditor /app/agents/ux_auditor
ENV PYTHONPATH=/app
CMD ["python", "agents/ux_auditor/auditor.py"]
