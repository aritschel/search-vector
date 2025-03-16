FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/services


COPY services /app/services

RUN pip install -r /app/services/api/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "services.api.search_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
