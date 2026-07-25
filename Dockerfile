FROM python:3.13-slim

RUN pip install --no-cache-dir fastapi uvicorn
RUN pip install ai-config-gen

WORKDIR /app
EXPOSE 8011

CMD ["uvicorn", "ai_config_gen.web_server:app", "--host", "0.0.0.0", "--port", "8011"]