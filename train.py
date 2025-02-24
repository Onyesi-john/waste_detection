from ultralytics import YOLO

# Load a model
model = YOLO("yolov5nu.pt")

# Train the model
model.train(
    data="/home/circleci/project/dataset/data.yaml",  # Relative path to data.yaml
    epochs=50,  # Changed from 15 to 50
    imgsz=416,
    batch=8,
    workers=2
)

# The best model is automatically saved to runs/detect/train/weights/best.pt
print("Training completed. Best model saved to runs/detect/train/weights/best.pt")