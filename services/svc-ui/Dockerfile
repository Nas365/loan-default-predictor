FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 STREAMLIT_SERVER_HEADLESS=true
WORKDIR /app
COPY services/svc-ui/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY services/svc-ui/ ./services/svc-ui/
COPY artifacts/ ./artifacts/
EXPOSE 8501
CMD ["streamlit", "run", "services/svc-ui/streamlit_app.py",
     "--server.port=8501",
     "--server.address=0.0.0.0",
     "--server.enableCORS=false",
     "--server.enableXsrfProtection=false",
     "--browser.gatherUsageStats=false"]

