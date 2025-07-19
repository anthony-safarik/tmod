import os

def remove_empty_folders(directory):
    """Recursively removes all empty folders and subfolders within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if the folder is empty
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")

def remove_empty_folders_and_ds_store(directory):
    """Recursively removes all .DS_Store files and empty folders/subfolders within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        # Remove .DS_Store files
        for file_name in files:
            if file_name == '.DS_Store' or file_name == 'Thumbs.db' or file_name == '.picasa.ini':
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Removed .DS_Store file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        # Remove empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Now this check is more accurate post .DS_Store removal
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to remove {dir_path}: {e}")


# Prompt user for directory path
directory_to_clean = input("Enter the path of the directory you want to clean up: ").strip()

# Confirm before executing
confirmation = input(f"Are you sure you want to remove all empty folders within and including '{directory_to_clean}'? (y/n): ").strip().lower()
if confirmation == "y":
    remove_empty_folders_and_ds_store(directory_to_clean)
    if not os.listdir(directory_to_clean): os.rmdir(directory_to_clean)
else:
    print("Operation cancelled.")
