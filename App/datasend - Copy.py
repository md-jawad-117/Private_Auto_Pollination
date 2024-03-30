import cv2
from ultralytics import YOLO
import time

# Initialize set to keep track of printed IDs
printed_ids = set()

# Function to handle mouse clicks
def click_event(event, x, y, flags, params):
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Pixel coordinates: (X: {x}, Y: {y})")

# Load the YOLOv8 model
model = YOLO("E:/Research_Papers/weed_detect/Yolo/Yolov8/Yolov8_nano_640/weights/best.onnx")
video_path = 'E:/Research_Papers/weed_detect/VIDEO/videos.mp4'
cap = cv2.VideoCapture(video_path)

# Initialize FPS calculation variables
prev_frame_time = 0
fps_sum = 0
frame_count = 0

# Loop through the video frames
while cap.isOpened():
    new_frame_time = time.time()
    success, frame = cap.read()

    # Check if frame is successfully read
    if not success:
        break

    cropped_frame = frame[224:480, :]
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(cropped_frame, persist=True, conf=0.7, iou=0.5, imgsz=(256, 640), verbose=False)
    output_tensor = results[0].boxes.id
    if output_tensor is not None:
        output_integers_id = [int(x) for x in output_tensor]
        output_tensor_box = results[0].boxes.xyxy
        output_integers_box = [[int(round(float(value))) for value in tensor] for tensor in output_tensor_box]
        print(output_integers_box)
        # Iterate over the IDs and their corresponding boxes
        for obj_id, bbox in zip(output_integers_id, output_integers_box):
            # Check if the ID has already been printed
            if obj_id not in printed_ids:
                selected_id=obj_id
                print(selected_id)
                centerX = (bbox[0] + bbox[2]) // 2  #x1,x2
                centerY = (bbox[1] + bbox[3]) // 2  #y1,y2
                
                wi=bbox[2] - bbox[0]
                hi = bbox[3] - bbox[1]
                area = wi*hi
                if area >20500:
                    # print(area)
                    print(len(printed_ids))
                    deltaX, deltaY = centerX, centerY
                    # Print the ID and its center point
                    # print(f"ID: {obj_id}, Center Point: ({deltaX}, {deltaY})")
                    # Add the ID to the set so it's not printed again
                    printed_ids.add(obj_id)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    # print(printed_ids)

    # Calculate and display FPS
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps_sum += fps
    frame_count += 1
    avg_fps = fps_sum / frame_count
    cv2.rectangle(annotated_frame, (0,0), (640,30), (255,255,255), thickness=-1)
    cv2.putText(annotated_frame, f'Weed Count:{len(printed_ids)}   'f'FPS:{fps:.1f}  'f'Avg FPS:{avg_fps:.0f}', (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (10, 10, 10), 2)
    

    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking", annotated_frame)

    # Set the click event listener for the window
    cv2.setMouseCallback("YOLOv8 Tracking", click_event)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
