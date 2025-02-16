# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install required system libraries
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

# Copy application files
COPY app.py /app/
COPY requirements.txt /app/
COPY best.pt /app/best.pt  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set model path as environment variable
ENV MODEL_PATH="/app/best.pt"

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
