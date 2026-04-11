# Dockerfile

# Use the Python 3.11-slim base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl --fail http://127.0.0.1:8000/health || exit 1

# Run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]