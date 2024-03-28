import os

def count_instances(folder_path):
    # Initialize counters for each class
    class_0_count = 0
    class_1_count = 0
    class_2_count = 0
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a text file
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            # Read lines from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()
            # Parse each line to extract class information
            for line in lines:
                line = line.strip().split()
                if len(line) > 0:
                    class_label = int(line[0])
                    # Update counters based on class label
                    if class_label == 0:
                        class_0_count += 1
                    elif class_label == 1:
                        class_1_count += 1
                    elif class_label == 2:
                        class_2_count += 1
    
    return class_0_count, class_1_count, class_2_count

# Example usage:
folder_location = "E:/Research_Papers/Autonomous Pollination/Dataset/aug/Final/valid/labels"
class_0_count, class_1_count, class_2_count = count_instances(folder_location)
print("Number of instances for class 0:", class_0_count)
print("Number of instances for class 1:", class_1_count)
print("Number of instances for class 2:", class_2_count)
