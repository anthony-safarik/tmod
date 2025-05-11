from examples.discoverfolders import discover_folders
from examples.rcopy import rcopy

if __name__ == "__main__":
    # Photos are in a DCIM folder for Sony cameras
    search_pattern = "/Volumes/*/DCIM"
    sync_folder = "/Volumes/X9Pro4TB/SYNC"

    # Discover folders
    found_folders = discover_folders(search_pattern)

    if len(found_folders) == 1:
        print (found_folders[0])
        rcopy(found_folders[0], sync_folder, ["-rav"])