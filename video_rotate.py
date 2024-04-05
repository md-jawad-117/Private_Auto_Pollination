import cv2

def flip_video(input_video_path, output_video_path):
    # Open the input video file
    video_capture = cv2.VideoCapture(input_video_path)
    
    # Get the video properties
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (height, width))
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Rotate the frame 90 degrees counterclockwise
        rotated_frame = cv2.transpose(frame)
        rotated_frame = cv2.flip(rotated_frame, 0)
        
        # Write the rotated frame to the output video
        out.write(rotated_frame)
        
        cv2.imshow('Rotated Video', rotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the resources
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Paths to input and output videos
input_video_path = "E:/Research_Papers/Autonomous Pollination/Resource/Video_image/video_F_.mp4"
output_video_path = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/videol_r.mp4'

# Call the function to flip the video
flip_video(input_video_path, output_video_path)
