FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY services/svc_api/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY services/svc_api/ ./services/svc_api/
COPY artifacts/ ./artifacts/

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=5 CMD curl -fsS http://localhost:8080/healthz || exit 1
CMD ["uvicorn", "services.svc_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
