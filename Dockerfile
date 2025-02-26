# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Copy the trained model into the container
COPY docker_model/best.pt /app/model/best.pt  # Adjust path if needed

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run (modify as needed)
CMD ["python", "app.py"]
