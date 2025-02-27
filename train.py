from ultralytics import YOLO

# Load the model
model = YOLO("yolov5nu.pt")

# Train the model
model.train(
    data="/home/circleci/project/dataset/data.yaml",  # Update this path
    epochs=50,
    batch=8,
    imgsz=416,
    project="/home/circleci/project/waste_detection",
    name="exp",
    exist_ok=True,
)