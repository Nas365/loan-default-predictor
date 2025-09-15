FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installig deps
COPY services/svc-ui/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copying model & app files
COPY artifacts/ ./artifacts/
COPY services/svc-ui/ ./services/svc-ui/

EXPOSE 8501
CMD ["sh", "-c", "streamlit run services/svc-ui/streamlit_app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
