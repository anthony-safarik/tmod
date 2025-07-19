import os
from pathlib import Path
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
import piexif

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.arw', '.dng'}

def get_exif_date(filepath):
    """Extract date photo was taken from EXIF data if available."""
    ext = filepath.suffix.lower()
    
    try:
        if ext in ['.jpg', '.jpeg']:
            img = Image.open(filepath)
            exif_data = img._getexif()
            if not exif_data:
                return None
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    return value
        elif ext in ['.arw', '.dng']:
            exif_dict = piexif.load(str(filepath))
            date_bytes = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
            if date_bytes:
                return date_bytes.decode()
    except Exception as e:
        print(f"Error reading EXIF from {filepath}: {e}")
    
    return None

def scan_directory_for_photos(directory):
    directory = Path(directory)
    print(f"Scanning directory: {directory}\n")

    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            date_taken = get_exif_date(file_path)
            if date_taken:
                print(f"{file_path} -> Taken on: {date_taken}")
            else:
                print(f"{file_path} -> Date taken: Not found")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search for photos and report date taken.")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()

    scan_directory_for_photos(args.directory)
