import os

def create_hard_link(source_path, destination_path):
    """
    Create a hard link pointing from destination_path to source_path.

    Parameters:
    - source_path (str): The path to the existing file.
    - destination_path (str): The path where the hard link will be created.

    Raises:
    - FileNotFoundError: If the source file does not exist.
    - FileExistsError: If the destination already exists.
    - OSError: For other OS-related errors (e.g., cross-device link).
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file does not exist: {source_path}")
    
    if os.path.exists(destination_path):
        raise FileExistsError(f"Destination already exists: {destination_path}")
    
    os.link(source_path, destination_path)
    print(f"Hard link created from '{source_path}' to '{destination_path}'")

if __name__ == "__main__":
    create_hard_link('/Users/tonysafarik/Downloads/PXL_20240902_001148925.jpg', '/Users/tonysafarik/Desktop/desktop-PXL_20240902_001148925.jpg')
