# Use the CircleCI Python image for compatibility
FROM cimg/python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Copy trained model to correct location
COPY docker_model/best.pt /app/model/best.pt  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for API if needed
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
