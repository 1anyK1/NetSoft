FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*    

RUN useradd -m -s /bin/bash service_user
WORKDIR /app
RUN chown -R service_user:service_user /app
USER service_user

RUN python3 -m venv venv

COPY requirements.txt .
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENV PATH="/app/venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
