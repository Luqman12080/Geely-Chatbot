# Use official slim Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching — only reinstalls if requirements change)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder into the container
COPY backend/ .

# Expose the port uvicorn will run on
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "chatbotAPI:app", "--host", "0.0.0.0", "--port", "8000"]