FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install system dependencies and Python packages in one layer to reduce size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip

# Copy application code
COPY . .

# Create directory for vector store
RUN mkdir -p Rag/vectorstore

# Expose port
EXPOSE 8005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8005/health')"

# Run the application
CMD ["uvicorn", "Backend.api.main:app", "--host", "0.0.0.0", "--port", "8005"]
