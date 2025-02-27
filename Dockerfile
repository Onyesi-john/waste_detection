# Use the CircleCI Python image for compatibility
FROM cimg/python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy necessary project files into the container
COPY static/ static/
COPY templates/ templates/
COPY app.py app.py


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the trained model into the container
COPY docker_model/best.pt /app/best.pt  

# Expose the port Flask will run on
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]
