FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and migrations
COPY . .
COPY alembic.ini .
RUN pip install -e .

# Create migrations directory if it doesn't exist
RUN mkdir -p migrations

# Initialize alembic if not already initialized
RUN if [ ! -f alembic.ini ]; then alembic init migrations; fi

# Run migrations at container startup instead of build time
EXPOSE 8000

# Use an entrypoint script to run migrations and start the app
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]