import os
import shutil
from pathlib import Path

CHUNK_SIZE_BYTES = 128 * 1000**3  # 128 GB
CHUNK_PREFIX = "PVA"
ACCEPTED_EXTENSIONS = ['.JPG', '.ARW', '.jpg', '.dng', '.MP4', '.DNG', '.mp4', '.SEC', '.MOV', '.AVI', '.mov', '.m4v', '.gif', '.MPG', '.psd', '.avi', '.jpeg', '.ASF', '.mpg', '.AAE', '.tif', '.PNG']

def get_all_files(source_dir):
    """
    Walk through the directory and collect all files with their sizes.
    Returns a list of tuples: (full_path, relative_path, size)
    """
    files = []
    for root, _, filenames in os.walk(source_dir):
        for name in filenames:
            extension_only = os.path.splitext(name)[1]
            if extension_only in ACCEPTED_EXTENSIONS and not name.startswith("."):
                full_path = os.path.join(root, name)
                rel_path = os.path.relpath(full_path, source_dir)
                size = os.path.getsize(full_path)
                files.append((full_path, rel_path, size))
    return files

def copy_to_chunk(chunk_dir, source_file, rel_path):
    """
    Copy file from source to chunk directory, preserving folder structure.
    """
    dest_file = os.path.join(chunk_dir, rel_path)
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    shutil.copy2(source_file, dest_file)

def create_chunks(source_dir, dest_dir, chunk_index = 1):
    files = get_all_files(source_dir)
    current_chunk_size = 0
    total_size = 0
    # chunk_dir = os.path.join(dest_dir, f"chunk_{chunk_index}")
    chunk_dir = os.path.join(dest_dir, f"{CHUNK_PREFIX}-{str(chunk_index).zfill(4)}", "ASSETS")

    for full_path, rel_path, size in files:
        # Start a new chunk if the current one would exceed 128GB
        if current_chunk_size + size > CHUNK_SIZE_BYTES:
            chunk_index += 1
            current_chunk_size = 0
            # chunk_dir = os.path.join(dest_dir, f"chunk_{chunk_index}")
            chunk_dir = os.path.join(dest_dir, f"{CHUNK_PREFIX}-{str(chunk_index).zfill(4)}", "ASSETS")

        print(f"Adding {rel_path} ({size / (1000 ** 3):.2f} GB) to chunk {chunk_dir})... chunk is {current_chunk_size / CHUNK_SIZE_BYTES:.2f} % full ")
        copy_to_chunk(chunk_dir, full_path, rel_path)
        current_chunk_size += size
        total_size += size

    print(f"\nCompleted: {chunk_index} chunk(s) created. Total size: {total_size / (1000 ** 4):.2f} TB")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Separate files into archive chunks.")
    parser.add_argument("source", help="Source directory path")
    parser.add_argument("destination", help="Destination directory path for chunks")
    parser.add_argument("start", nargs="?", help="Optional chunk start number")

    args = parser.parse_args()

    archive_start_num = 1
    if args.start:
        try:
            archive_start_num = int(args.start)
        except:
            pass

    if not os.path.isdir(args.source):
        print("Error: Source directory does not exist.")
    else:
        os.makedirs(args.destination, exist_ok=True)
        create_chunks(args.source, args.destination, archive_start_num)
