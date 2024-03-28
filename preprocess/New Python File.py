import os

def remove_images_without_annotations(folder_path):
    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is an image
        if file_name.endswith(".jpg") or file_name.endswith(".png") or file_name.endswith(".jpeg"):
            image_path = os.path.join(folder_path, file_name)
            # Check if corresponding text file exists
            base_name, _ = os.path.splitext(file_name)
            txt_file_path = os.path.join(folder_path, base_name + ".txt")
            if not os.path.exists(txt_file_path):
                print(f"Removing {image_path} as corresponding txt file does not exist.")
                os.remove(image_path)
# Provide the path to the folder containing the images and text files
folder_path = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/images"

# Call the function to remove images without annotations
remove_images_without_annotations(folder_path)
