# Use the CircleCI Python image for compatibility
FROM cimg/python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the project directory
COPY . .

# Install dependencies from both requirements files
RUN pip install --no-cache-dir -r yolov5/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the trained model into the container
COPY docker_model/best.pt /app/model/best.pt  

# Set the default command to run inference
CMD ["python", "detect.py", "--weights", "model/best.pt", "--source", "0"]
