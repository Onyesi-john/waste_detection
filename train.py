import os
from ultralytics import YOLO

# Define writable directory
output_directory = "/tmp/wastedetection"  # Updated directory name
os.makedirs(output_directory, exist_ok=True)

# Define model path
model_path = os.path.join(output_directory, "yolov5nu.pt")

# Load the model (ensure correct path)
model = YOLO(model_path) if os.path.exists(model_path) else YOLO("/home/john/models/yolov5n.pt")

# Train the model
model.train(
    data="data.yaml",
    epochs=50,
    imgsz=416,
    batch=8,
    workers=2,
    project=output_directory,  # Save training results here
    name="exp",  # Use "exp" to avoid empty subfolder issues
    exist_ok=True
)

print(f"Training completed. Best model saved to {output_directory}/exp/weights/best.pt")
