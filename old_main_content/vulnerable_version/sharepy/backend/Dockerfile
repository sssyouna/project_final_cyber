FROM python:3.11-slim

WORKDIR /app

# Install PHP CLI
RUN apt-get update && apt-get install -y php-cli && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# M13: chmod 777 on uploads directory
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# M2: Debug mode enabled in startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]