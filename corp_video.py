
import cv2

def crop_video(input_file, output_file, top_crop, bottom_crop):
    # Open the video file
    cap = cv2.VideoCapture(input_file)
    
    # Get the original width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the crop region
    y1 = top_crop
    y2 = height - bottom_crop
    x1 = 0
    x2 = width
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, 30, (x2 - x1, y2 - y1))
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Crop the frame
            cropped_frame = frame[y1:y2, x1:x2]
            
            # Write the cropped frame to the output video
            out.write(cropped_frame)
            
            # Display the cropped frame
            cv2.imshow('Cropped Video', cropped_frame)
            
            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Define input and output file paths
input_file = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/videol_r.mp4'
output_file = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/video_c.mp4'

# Define the number of pixels to crop from top and bottom
top_crop = 200
bottom_crop = 200

# Call the function to crop the video
crop_video(input_file, output_file, top_crop, bottom_crop)

