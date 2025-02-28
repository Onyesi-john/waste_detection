# Use the ARM-compatible Python image for Raspberry Pi compatibility
FROM arm64v8/python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the trained model into the container
COPY docker_model/best.pt /app/model/best.pt

# Set the default command to run inference
CMD ["python", "detect.py", "--weights", "model/best.pt", "--source", "0"]