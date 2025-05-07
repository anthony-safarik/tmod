import shutil
import os

def delete_directory(directory_path):
    """Deletes all contents of a directory and removes the directory itself."""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Deleted: {directory_path}")
    else:
        print(f"Directory not found: {directory_path}")

# Prompt user for directory path
directory_to_delete = input("Enter the path of the directory you want to delete: ").strip()

# Confirm before executing
confirmation = input(f"Are you sure you want to delete '{directory_to_delete}'? (y/n): ").strip().lower()
if confirmation == "y":
    delete_directory(directory_to_delete)
else:
    print("Operation cancelled.")
