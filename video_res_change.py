import cv2

def resize_video(input_video_path, output_video_path, new_width, new_height):
    # Open the input video file
    video_capture = cv2.VideoCapture(input_video_path)
    
    # Get the original video properties
    original_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Resize the frame
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        # Write the resized frame to the output video
        out.write(resized_frame)
        
        cv2.imshow('Resized Video', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the resources
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

# Paths to input and output videos
input_video_path = "E:/Research_Papers/Autonomous Pollination/Resource/Video_image/videol_r.mp4"
output_video_path = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/video_256x640.mp4'

# Get new resolution from user input
new_width = 480
new_height = 640

# Call the function to resize the video
resize_video(input_video_path, output_video_path, new_width, new_height)
