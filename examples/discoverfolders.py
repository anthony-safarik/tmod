import glob
import os

def discover_folders(pattern):
    """
    Discover folders matching the given pattern.
    
    :param pattern: A filesystem path pattern with wildcards (*).
    :return: List of matching folder paths.
    """
    matching_folders = glob.glob(pattern)

    # Ensure only directories are included
    matching_folders = [folder for folder in matching_folders if os.path.isdir(folder)]
    
    return matching_folders

if __name__ == "__main__":
    # Define the search pattern
    search_pattern = "/Volumes/*/Users/*/Desktop"

    # Discover folders
    found_folders = discover_folders(search_pattern)

    # Print results
    if found_folders:
        print("Discovered folders:")
        for folder in found_folders:
            print(folder)
    else:
        print("No matching folders found.")
