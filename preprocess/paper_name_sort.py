import os

folder_path = "E:\Research_Papers\weed_detect\Paper"  # Replace with the path to your folder containing the PDF files

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Sort the file list in ascending order
file_list.sort()

# Iterate over the files and rename them
for i, file_name in enumerate(file_list):
    if file_name.endswith(".pdf"):
        new_name = f"P{i+1}_{file_name}"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {file_name} -> {new_name}")
