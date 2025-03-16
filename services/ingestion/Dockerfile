FROM python:3.9-slim

WORKDIR /app/services

COPY services /app/services

RUN pip install -r /app/services/ingestion/requirements.txt

EXPOSE 8001

CMD ["uvicorn", "services.ingestion.ingestion_service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
