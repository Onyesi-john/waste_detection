from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")  # Update if you use a different weight file

# Train model
model.train(data="dataset/data.yaml", epochs=50, imgsz=640)

print("✅ Training completed!")
