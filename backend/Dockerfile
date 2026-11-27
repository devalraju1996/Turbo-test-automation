
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends libatomic1 && rm -rf /var/lib/apt/lists/*
RUN playwright install --with-deps chromium

COPY backend/app ./app
COPY automation ./automation

ENV PYTHONPATH=/app/automation
ENV BASE_URL=http://frontend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
