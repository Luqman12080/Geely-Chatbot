# Use official slim Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (assumes requirements.txt is at repo root)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend folder into /app/backend (preserve the folder structure)
COPY backend/ ./backend/

# Expose the port uvicorn will run on
EXPOSE 8000

# Point uvicorn to the module using dot notation: folder.filename:app_instance
CMD ["uvicorn", "backend.chatbotAPI:app", "--host", "0.0.0.0", "--port", "8000"]