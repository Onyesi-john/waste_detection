from ultralytics import YOLO

# Load a model
model = YOLO("yolov5nu.pt")

# Train the model
model.train(
    data="dataset/data.yaml",
    epochs=15,
    imgsz=416,
    batch=8,
    workers=2
)

# The best model is automatically saved to runs/detect/train/weights/best.pt
print("Training completed. Best model saved to runs/detect/train/weights/best.pt")