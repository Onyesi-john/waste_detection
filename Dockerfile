# Use an official lightweight Python image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy model weights (Make sure `best.pt` is in your project)
COPY best.pt /app/best.pt

# Expose port for the application
EXPOSE 5000

# Run the app (change based on your project)
CMD ["python", "app.py"]
