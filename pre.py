from ultralytics import YOLO
import cv2

model = YOLO("/home/john/waste_detection/yolov5/runs/train/exp/weights/best.pt")
results = model("/home/john/waste_detection/dataset/valid/images/Banana_1_jpg.rf.0fcc3cf0ff574bc791690456f90e8c06.jpg")  # Test with an image from your dataset

for r in results:
    r.show()  # Display the results
