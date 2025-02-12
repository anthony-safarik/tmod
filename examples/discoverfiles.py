import glob
import os

def discover_files(pattern):
    """
    Discover files matching the given pattern.
    
    :param pattern: A filesystem path pattern with wildcards (*).
    :return: List of matching file paths.
    """
    matching_files = glob.glob(pattern)

    # Ensure only directories are included
    matching_files = [file for file in matching_files if os.path.isfile(file)]
    
    return matching_files

if __name__ == "__main__":
    # Define the search pattern
    search_pattern = "/Volumes/*/Users/*/Desktop/Screen*"

    # Discover files
    found_files = discover_files(search_pattern)

    # Print results
    if found_files:
        print("Discovered files:")
        for file in found_files:
            print(file)
            # I dislike all the spaces and dots in Mac Screenshots.
            bname = os.path.basename(file)
            newname = bname.replace(' ','_').replace('.', '-', 2)
            print(newname)

    else:
        print("No matching files found.")
