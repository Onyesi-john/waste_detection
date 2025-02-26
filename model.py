from ultralytics import YOLO

# Load the trained model
model_path = "/home/john/waste_detection/waste_detection/exp/weights/best.pt"
model = YOLO(model_path)  # Use YOLO class from Ultralytics

# Print model details
print("Model information:", model.model)
print("Model YAML:", model.model.yaml)  # This will show architecture details
