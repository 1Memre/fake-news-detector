FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

# Copy the backend code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
# We use "main:app" assuming the Docker context is inside /backend or we adjust imports.
# Based on project structure: /backend/main.py. 
# If we run from root context in compose, it copies everything.
# Let's assume this Dockerfile is placed in /backend/ and context is /backend/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
