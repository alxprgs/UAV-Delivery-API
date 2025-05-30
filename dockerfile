FROM python:3.13.0-slim

HEALTHCHECK --interval=30s CMD curl -f http://localhost:$SERVER_PORT/health || exit 1


RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SERVER_PORT=${SERVER_PORT}

EXPOSE ${SERVER_PORT}
CMD ["python", "run.py"]