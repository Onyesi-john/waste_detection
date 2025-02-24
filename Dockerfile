# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy requirements first to optimize Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the trained model
COPY best.pt /app/best.pt

# Copy the rest of the application code
COPY . /app

# Expose port (if needed for a web app)
EXPOSE 5000

# Set the default command
CMD ["python", "app.py"]
