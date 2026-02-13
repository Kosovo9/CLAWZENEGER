FROM python:3.11-slim
WORKDIR /app
COPY agents/offer_validator/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY agents/offer_validator /app/agents/offer_validator
ENV PYTHONPATH=/app
CMD ["python", "agents/offer_validator/validator.py"]
