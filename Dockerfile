# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/uploads /app/processed

# Expose port for the application
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
