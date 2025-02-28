# Use the CircleCI Python image for compatibility
FROM cimg/python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model into the container
COPY best.pt /app/model/best.pt  

# Expose port for web access (e.g., Flask/FastAPI)
EXPOSE 5000

# Set the default command to run the application
CMD ["python", "app.py"]
