# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Ensure the model directory exists before copying
RUN mkdir -p /app/model

# Copy the trained model into the container
COPY docker_model/best.pt /app/model/  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run (modify as needed)
CMD ["python", "app.py"]
