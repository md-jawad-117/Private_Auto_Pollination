import cv2
from ultralytics import YOLO
import time
import serial
# ser = serial.Serial('COM7', 9600)
# Initialize set to keep track of printed IDs
printed_ids = set()       

counter=0

# Load the YOLOv8 model
model = YOLO("E:/Research_Papers/Autonomous Pollination/model/best.pt")
video_path = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/video_480x640.mp4'
cap = cv2.VideoCapture(video_path)

# Initialize FPS calculation variables

# Loop through the video frames
while cap.isOpened():
    success, frame = cap.read()

    # Check if frame is successfully read
    if not success:
        break

    cropped_frame = frame[:, 224:480]
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(cropped_frame, persist=True, conf=0.7, iou=0.5, imgsz=(640, 256), verbose=False, classes=1)
    output_tensor = results[0].boxes.id     # boxes is paramter while id is attribute.
    if output_tensor is not None:
        output_integers_id = [int(x) for x in output_tensor]
        output_tensor_box = results[0].boxes.xyxy
        output_integers_box = [[int(round(float(value))) for value in tensor] for tensor in output_tensor_box]
        # print(output_integers_id)
        unchecked_num = [num for num in output_integers_id if num not in printed_ids]
        if unchecked_num:
            choosen_value = min(unchecked_num)
            bbox = None  # Initialize bbox variable outside the loop
            while counter < 30:
                success, frame = cap.read()
                if not success:
                    break  # Break the loop if frame is not successfully read

                cropped_frame = frame[:,224 :480]
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = model.track(cropped_frame, persist=True, conf=0.7, iou=0.5, imgsz=(640, 256), verbose=False, classes=1)
                
                output_tensor = results[0].boxes.id
                if output_tensor is not None:
                    output_integers_id = [int(x) for x in output_tensor]
                    output_tensor_box = results[0].boxes.xyxy
                    output_integers_box = [[int(round(float(value))) for value in tensor] for tensor in output_tensor_box]

                    try:
                        # Find the index of the object with the specified ID
                        index = output_integers_id.index(choosen_value)
                        # Get the corresponding bounding box value
                        bbox = output_integers_box[index]
                        # Print the bounding box for debugging
                        centerX = (bbox[0] + bbox[2]) // 2
                        centerY = (bbox[1] + bbox[3]) // 2
                        print(centerX, centerY)
                        # ser.write(f"{centerX},{centerY}\n".encode())
                        # print("Bounding box for object with ID",counter,"--", choosen_value, ":", bbox)
                        annotated_frame = results[0].plot()
                        cv2.imshow("YOLOv8 Tracking", annotated_frame)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            break
                    except ValueError:
                        annotated_frame = results[0].plot()
                        cv2.imshow("YOLOv8 Tracking", annotated_frame)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            break
                counter += 1
                    
            counter=0
            printed_ids.add(choosen_value)

    annotated_frame = results[0].plot()
    
    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
