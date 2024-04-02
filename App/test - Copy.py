import cv2

# Load the image
image = cv2.imread("E:/Research_Papers/Autonomous Pollination/Resource/Heatmap Image/2.jpg")  # Replace 'path_to_your_image.jpg' with the actual path to your image file

# Check if the image was successfully loaded
if image is None:
    print('Error: Image not found or unable to load.')
else:
    
    cropped_image = image[:, 224:640]# Display the image  #h x w  640 x 480
    cv2.imshow('Image', cropped_image)
    cv2.waitKey(0)  # Wait indefinitely until any key is pressed
    cv2.destroyAllWindows()  # Close all OpenCV windows
