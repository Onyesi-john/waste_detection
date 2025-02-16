# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

# Copy project files
COPY app.py /app/
COPY requirements.txt /app/

# Copy the latest model (Jenkins ensures the correct file is here)
COPY best.pt /app/best.pt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Set model path as environment variable
ENV MODEL_PATH="/app/best.pt"


# Expose port (change based on your app)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
