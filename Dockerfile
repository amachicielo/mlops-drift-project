FROM python:3.10-slim

WORKDIR /app

# 🔧 Add these system dependencies before pip install
RUN apt-get update && apt-get install -y \
    tk \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
