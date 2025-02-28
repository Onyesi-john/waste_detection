# Use CircleCI's Python image for compatibility
FROM cimg/python:3.9

# Set working directory
WORKDIR /app

# Copy only essential project files (excluding datasets)
COPY app.py requirements.txt static/ templates/ ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model (best.pt) into the /app folder
COPY best.pt /app/best.pt  

# Expose port for web access (e.g., Flask/FastAPI)
EXPOSE 5000

# Set the default command to run the application
CMD ["python", "app.py"]
