# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies (Tesseract + libraries)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port (5000)
EXPOSE 5000

# Start your Flask server
CMD ["python", "Server.py"]
