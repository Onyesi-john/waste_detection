from ultralytics import YOLO

# Load the YOLOv5n model
model = YOLO("yolov5n.pt")

# Train the model
model.train(
    data="/home/circleci/project/dataset/data.yaml",  # Absolute path to data.yaml
    epochs=50,
    imgsz=640,
    batch=8,
    project="/home/circleci/project/waste_detection",  # Save outputs inside the working directory
    name="exp",
    exist_ok=True,
)
