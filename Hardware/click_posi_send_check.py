import cv2
import serial

ser = serial.Serial('COM6', 9600)

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked position: (X: {x}, Y: {y})")
        ser.write(f"{x},{y}\n".encode())

cap = cv2.VideoCapture(0)

cv2.namedWindow("Webcam Feed")
cv2.setMouseCallback("Webcam Feed", click_event)

while True:
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = frame[:, :]
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    height, width = frame.shape[:2]
    center_coordinates = (width // 2, height // 2)

    dot_color = (0, 0, 255) # Red color in BGR
    dot_size = 5
    cv2.circle(frame, center_coordinates, dot_size, dot_color, -1)

    line_color = (0, 255, 0) # Green color in BGR
    cv2.line(frame, (0, center_coordinates[1]), (width, center_coordinates[1]), line_color, 1)
    cv2.line(frame, (center_coordinates[0], 0), (center_coordinates[0], height), line_color, 1)

    cv2.imshow('Webcam Feed', frame)

    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
ser.close()
