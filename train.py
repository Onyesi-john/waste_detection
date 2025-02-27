import os

# Define dataset path
dataset_path = "dataset/data.yaml"

# Train YOLOv5 using CLI command
os.system(f"python yolov5/train.py --img 416 --batch 8 --epochs 50 --data {dataset_path} --weights yolov5n.pt --project runs/train/ --name exp")
