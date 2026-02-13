FROM python:3.11-slim
WORKDIR /app
COPY agents/sales_closer/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY agents/sales_closer /app/agents/sales_closer
ENV PYTHONPATH=/app
CMD ["python", "agents/sales_closer/closer.py"]
