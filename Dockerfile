# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create uploads and processed directories
RUN mkdir -p /app/uploads /app/processed

# Expose port for the application
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]