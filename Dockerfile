FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN pip install -e .

# Run migrations
RUN alembic upgrade head

EXPOSE 8000

CMD ["uvicorn", "fastyr.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 