from ultralytics import YOLO
import cv2
import math
import os

# Function to calculate IoU
def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    union_area = box1_area + box2_area - intersection_area

    iou = intersection_area / union_area if union_area > 0 else 0
    return iou

# Load image and annotation
image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/1.jpg'  # Provide the path to your image
# image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/2.jpeg'  # Provide the path to your image
# image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/3.jpeg'  # Provide the path to your image
# image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/4.jpg'  # Provide the path to your image
# image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/5.jpg'  # Provide the path to your image
# image_path = 'E:/Research_Papers/weed_detect/images/Containing Folder/External/6.jpg'  # Provide the path to your image




annotation_path = os.path.splitext(image_path)[0] + '.txt'  # Assuming annotation file has the same name but with '.txt' extension

# Load image
img = cv2.imread(image_path)

# Load model
model = YOLO("E:/Research_Papers/weed_detect/Models/small_cbam_c3tr_15k.pt")

# Load object classes
classNames = ['Waterhemp', 'MorningGlory', 'Purslane', 'SpottedSpurge', 'Carpetweed', 'Ragweed', 'Eclipta', 'PricklySida', 'PalmerAmaranth', 'Sicklepod', 'Goosegrass', 'Cutleaf']
img = cv2.resize(img, (640, 640))
# Perform object detection
results = model(img)
font = cv2.FONT_HERSHEY_SIMPLEX
# Draw predicted bounding boxes
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
        confidence = math.ceil((box.conf[0]*100))
        cls = int(box.cls[0])
        cv2.putText(img, f'{classNames[cls]}: {confidence}%', (int(5), int(35)), font, 1.4, (0, 0, 0), 2, cv2.LINE_AA)

# Draw ground truth bounding box from annotation file
if os.path.exists(annotation_path):
    with open(annotation_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.split()
            class_index = int(values[0])
            x_center, y_center, width, height = map(float, values[1:])
            
            # Convert to pixel values
            h, w, _ = img.shape
            x, y, w, h = int((x_center - width/2) * w), int((y_center - height/2) * h), int(width * w), int(height * h)
            
            # Draw ground truth bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 4)

            # Calculate IoU
            iou = calculate_iou([x1, y1, x2, y2], [x, y, x + w, y + h])

            # Display IoU on the image
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(img, f'IoU: {iou:.4f}', (int(x+5), int(y + h-10)), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

# Resize the image to 640x640
resized_img = cv2.resize(img, (640, 640))

# Display the resized image with bounding boxes and IoU
cv2.imshow('Resized Image with Bounding Boxes and IoU', resized_img)

# Save the resized image
cv2.imwrite('E:/Research_Papers/weed_detect/images/Containing Folder/External/small_c3tr_1.png', resized_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
