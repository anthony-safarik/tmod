import os
from pathlib import Path
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import hashlib


SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg'}


def get_exif_data(filepath):
    """Extract date photo was taken from EXIF data if available."""

    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        if not exif_data:
            return None
        else:
            return exif_data.items()

    except Exception as e:
        print(f"Error reading EXIF from {filepath}: {e}")
    
    return None

# def scan_directory_for_photos(directory):
#     directory = Path(directory)
#     print(f"Scanning directory: {directory}\n")

#     for file_path in directory.rglob("*"):
#         if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
#             get_exif_data(file_path)

            

if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(description="Search for photos and report date taken.")
    # parser.add_argument("directory", help="Directory to scan")
    # args = parser.parse_args()

    # scan_directory_for_photos(args.directory)
    data = get_exif_data("/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0048/assets/PHOTOS/2017/2017-09-16/DSC07192.JPG")
    for k, v in data:
        tag = TAGS.get(k, k)
        print(tag,v)