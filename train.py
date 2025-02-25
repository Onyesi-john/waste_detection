from ultralytics import YOLO

# Load a model
model = YOLO("/home/john/waste_detection/yolov5nu")

# Train the model
model.train(
    data="/home/john/waste_detection/dataset/data.yaml",  # Relative path to data.yaml
    epochs=50,  # Changed from 15 to 50
    imgsz=416,
    batch=8,
    workers=2,
    project="./yolo5nu",  # Save results in the "yolo5nu" folder
    name="",  # Empty name to avoid subfolders
    exist_ok=True  # Overwrite existing files
)

# The best model is automatically saved to yolo5nu/weights/best.pt
print("Training completed. Best model saved to yolo5nu/weights/best.pt")