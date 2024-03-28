import os
import shutil
def process_images_with_empty_labels(image_folder, label_folder, output_folder, empty_label_output_folder):
    # Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(empty_label_output_folder, exist_ok=True)

    # Get a list of all YOLO label files in the label folder
    label_files = [file for file in os.listdir(label_folder) if file.endswith(".txt")]

    for label_file in label_files:
        label_path = os.path.join(label_folder, label_file)

        # Check if the label file is empty
        if os.path.getsize(label_path) == 0:
            # Move the empty label file to the specified output folder
            empty_label_output_path = os.path.join(empty_label_output_folder, label_file)
            shutil.move(label_path, empty_label_output_path)

            # Transfer the corresponding image to the output folder
            image_path = os.path.join(image_folder, label_file.replace(".txt", ".jpg"))
            output_image_path = os.path.join(output_folder, label_file.replace(".txt", ".jpg"))

            # Move the image file to the output folder
            shutil.move(image_path, output_image_path)

if __name__ == "__main__":
    # Set your image, label, output, and empty label output folder paths
    image_folder_path = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/images"
    label_folder_path = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/labels"
    output_folder_path = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/Final"
    empty_label_output_folder_path = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/Empty_Labels"

    process_images_with_empty_labels(image_folder_path, label_folder_path, output_folder_path, empty_label_output_folder_path)
