from ultralytics import YOLO
import os

# Define the project directory
project_dir = os.path.join(os.getcwd(), 'waste_detection')

# Load a model (ensure the correct file name & path)
model = YOLO('yolov5nu.pt')  # Change this to your actual file path

model.to('cpu')

# Train the model
model.train(
    data="/home/john/waste_detection/dataset/data.yaml",  
    epochs=50,  
    imgsz=416,
    batch=8,
    workers=2,
    project=project_dir,  # Save results in the waste_detection directory
    name="exp",  # Use "exp" instead of empty string to avoid errors
    exist_ok=True  
)

print(f"Training completed. Best model saved to {project_dir}/exp/weights/best.pt")
