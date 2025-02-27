# Use the CircleCI Python image for compatibility
FROM cimg/python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the project directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run inference
CMD ["python", "detect.py", "--weights", "runs/train/exp/weights/best.pt", "--source", "0"]
