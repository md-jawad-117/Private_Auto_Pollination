from ultralytics import YOLO
import cv2
import os
import math

# Load model
model = YOLO("E:/Research_Papers/Autonomous Pollination/model/best.pt")

classNames = ['0', '1', '2']
min_confidence = 0.75

# Folder path containing the images
folder_path = 'E:/Research_Papers/Autonomous Pollination/Dataset/aug/Final/valid/images/'

# Iterate over each image in the folder
for image_name in os.listdir(folder_path):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, image_name)
        image = cv2.imread(image_path)

        # Check if image is loaded successfully
        if image is None:
            print(f"Error opening image {image_name}")
            continue

        # Get image dimensions
        height, width, _ = image.shape

        results = model(image)
        # Prepare to write to annotation file
        annotation_path = os.path.splitext(image_path)[0] + '.txt'
        with open(annotation_path, 'w') as f:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    confidence = math.ceil((box.conf[0]*100))/100
                    if confidence >= min_confidence:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        # Normalize coordinates
                        x_center = ((x1 + x2) / 2) / width
                        y_center = ((y1 + y2) / 2) / height
                        bbox_width = (x2 - x1) / width
                        bbox_height = (y2 - y1) / height

                        # Write to file
                        f.write(f"{int(box.cls[0])} {x_center} {y_center} {bbox_width} {bbox_height}\n")

