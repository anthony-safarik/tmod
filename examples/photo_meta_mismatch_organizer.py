import os
from pathlib import Path
from datetime import datetime
import shutil
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

def parse_exif_date(date_str):
    """Convert EXIF date string to datetime object."""
    try:
        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception:
        return None

def organize_file(file_path, date_obj, output_root):
    """Create folders and rename the file based on date."""
    year = date_obj.strftime('%Y')
    date_folder = date_obj.strftime('%Y-%m-%d')
    filename = f"{date_obj.strftime('%Y%m%d')}-{file_path.name}"
    target_dir = output_root / year / date_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / filename

    # Avoid overwriting files
    if target_path.exists():
        print(f"File already exists: {target_path}, skipping.")
        return

    shutil.move(file_path, target_path)
    print(f"Moved: {file_path} -> {target_path}")

# def organize_mismatched_files(source_file_path, dest_root, date_obj):
#      """Create folders and rename the file based on datetime object."""
#      # for example source file "PHOTOS/2006/2006-07-08/20060708-IMG_1039.JPG" Taken on: 2006:09:30 09:38:27 --> <dest_root>/2006/2006-09-30/20060930-IMG_1039.JPG


def organize_mismatched_files(source_file_path, dest_root, date_obj):
    """Create folders and rename the file based on datetime object."""
    
    # Extract the original filename
    original_filename = os.path.basename(source_file_path)
    
    # Get the filename suffix (e.g., -IMG_1039.JPG)
    if '-' in original_filename:
        suffix = original_filename[original_filename.index('-'):]  # e.g. -IMG_1039.JPG
    else:
        suffix = "-" + original_filename  # Fallback
    
    # Format date for folder and filename
    year = date_obj.strftime("%Y")
    date_str = date_obj.strftime("%Y-%m-%d")
    date_prefix = date_obj.strftime("%Y%m%d")
    
    # Construct destination directory and file path
    dest_dir = os.path.join(dest_root, year, date_str)
    os.makedirs(dest_dir, exist_ok=True)
    
    new_filename = date_prefix + suffix
    dest_file_path = os.path.join(dest_dir, new_filename)
    
    # Move and rename the file
    shutil.move(source_file_path, dest_file_path)

    return dest_file_path


def scan_directory_for_photos(input_dir, output_dir=None):
    input_dir = Path(input_dir)
    print(f"\nScanning directory: {input_dir}\n")

    for file_path in input_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            date_taken_str = get_exif_date(file_path)
            # date_taken_str_readable = date_taken_str.split()[0].replace(':','-')

            folder_date = get_date_file_path(file_path)

            if date_taken_str:
                date_obj = parse_exif_date(date_taken_str)
                # date_taken_str_readable = date_taken_str.split()[0].replace(':','-')
                # if date_taken_str_readable != folder_date:
                # if output_dir and date_obj and date_taken_str_readable != folder_date:
                if output_dir and date_obj:
                    org_file = organize_mismatched_files(file_path, Path(output_dir), date_obj)
                    print(f"{file_path} -> {org_file}")
                else:
                    # print(f"{file_path} -> Taken on: {date_taken_str} Lives in: {folder_date}")
                    if date_taken_str:
                        print(date_taken_str)
                        # date_taken_str_readable = date_taken_str.split()[0].replace(':','-')
                        if date_taken_str_readable != folder_date:
                            
                            print(f"{file_path} -> Taken on:  Lives in: {folder_date}")

            # else:
            #     print(f"{file_path} -> Date taken: Not found")



def get_date_renamed_file_path(file_path):
    fp_dir = os.path.dirname(file_path)
    fp_basename = os.path.basename(file_path)
    fp_parent = os.path.basename(fp_dir)
    if len(fp_parent) >= 10:
        date_string = fp_parent[:10].replace('-','') + '-'
        renamed_path = os.path.join(fp_dir, date_string + fp_basename)
        return renamed_path

def get_date_file_path(file_path):
    fp_dir = os.path.dirname(file_path)
    fp_basename = os.path.basename(file_path)
    fp_parent = os.path.basename(fp_dir)
    if len(fp_parent) >= 10:
        # date_string = fp_parent[:10].replace('-','') + '-'
        # renamed_path = os.path.join(fp_dir, date_string + fp_basename)
        return fp_parent[:10]



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search for photos and optionally rename/organize them by date taken.")
    parser.add_argument("input_dir", help="Directory to scan for photos")
    parser.add_argument("output_dir", nargs="?", help="Optional directory to organize/rename photos into")
    args = parser.parse_args()

    scan_directory_for_photos(args.input_dir, args.output_dir)
