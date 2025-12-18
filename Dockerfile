# Use official Python image
FROM python:3.11-slim

# Set working directory inside container to /app/Authentication
WORKDIR /app/Authentication

# Copy requirements first (better caching)
COPY Authentication/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Authentication folder into container
COPY Authentication/ .

# Expose FastAPI port
EXPOSE 8009

# Run FastAPI with uvicorn (same as you do locally)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]
