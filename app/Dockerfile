# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Ensure best.pt is included
RUN if [ ! -f "best.pt" ]; then echo "❌ Error: best.pt not found!"; exit 1; fi

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the model service
CMD ["python", "inference.py"]
