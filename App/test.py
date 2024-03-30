import cv2

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Rotate the frame by 180 degrees
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Merge the original and rotated frames
        merged_image = cv2.hconcat([frame, rotated_frame])

        # Display the merged image
        cv2.imshow('Merged Image', merged_image)

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
