import os
from pathlib import Path
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import hashlib
import csv
import shutil

# SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.arw', '.dng'}
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg'}

def get_file_size(file_path):
    """
    Returns the size of the file at the given file_path in bytes.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist or is not a regular file.")
    
    return os.path.getsize(file_path)


def calc_md5(file_path):
    """Calculate the MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

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

from PIL import Image
import piexif

def get_image_resolution(filepath):
    """
    Extract the resolution (width x height) of an image from metadata or image file.
    Returns a tuple: (width, height) or None if it cannot be determined.
    """
    ext = filepath.suffix.lower()

    try:
        if ext in ['.jpg', '.jpeg']:
            img = Image.open(filepath)
            return img.size  # (width, height)
        
        elif ext in ['.arw', '.dng']:
            # For raw formats, try reading via piexif (if any preview image metadata is available)
            exif_dict = piexif.load(str(filepath))
            width = exif_dict['0th'].get(piexif.ImageIFD.ImageWidth)
            height = exif_dict['0th'].get(piexif.ImageIFD.ImageLength)

            if width and height:
                return (width, height)

            # If EXIF doesn't contain dimensions, fall back to PIL
            img = Image.open(filepath)
            return img.size

    except Exception as e:
        print(f"Error reading resolution from {filepath}: {e}")

    return None

def scan_directory_for_photos(directory, output_csv="photo_metadata.csv"):
    directory = Path(directory)
    print(f"Scanning directory: {directory}\n")

    # Open CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_path', 'date_taken', 'resolution', 'md5', 'file_size']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_path in directory.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.name.startswith("._"):
                continue  # Skip macOS dot-underscore files

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            date_taken = get_exif_date(file_path)
            resolution = get_image_resolution(file_path)
            md5 = calc_md5(file_path)
            file_size = get_file_size(file_path)

            writer.writerow({
                'file_path': str(file_path),
                'date_taken': date_taken if date_taken else 'XXXX',
                'resolution': f"{resolution[0]}x{resolution[1]}" if resolution else '0x0',
                'md5': md5 if md5 else 'null',
                'file_size': file_size if file_size else 'null'
            })

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search for photos and report date taken.")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()

    scan_directory_for_photos(args.directory)
    shutil.copy2("photo_metadata.csv", f"photo_metadata_{args.directory.replace('/','-')}.csv")
