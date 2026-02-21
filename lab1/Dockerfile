FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

RUN useradd -m -s /bin/bash service_user && chown -R service_user:service_user /app && apt-get update && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -r requirements.txt  

USER service_user

COPY . .

EXPOSE 8000
ENV PATH="/app/venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
