from ultralytics import YOLO

# Load a model (ensure the correct file name & path)
model = YOLO("/home/john/waste_detection/yolov5nu")  # Change this to your actual file path

# Train the model
model.train(
    data="/home/john/waste_detection/dataset/data.yaml",  
    epochs=50,  
    imgsz=416,
    batch=8,
    workers=2,
     
)

print("Training completed. Best model saved to yolo5nu/weights/best.pt")