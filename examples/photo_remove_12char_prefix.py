import os
import re

def rename_files_in_directory(directory):
    # Regular expression to match 12-digit prefix followed by underscore
    pattern = re.compile(r'^\d{12}_')

    for filename in os.listdir(directory):
        # Match only files with the 12-digit prefix
        if pattern.match(filename):
            new_filename = pattern.sub('', filename)  # Remove the prefix
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f'Renamed: {old_path} -> {new_path}')

if __name__ == "__main__":
    target_directory = input("Enter the path to the directory: ").strip()
    if os.path.isdir(target_directory):
        rename_files_in_directory(target_directory)
    else:
        print("Invalid directory path.")
