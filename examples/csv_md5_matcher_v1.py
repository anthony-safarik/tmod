import os
import hashlib
import csv
import argparse
import shutil
import time

def remove_empty_folders_and_ds_store(directory):
    """Recursively removes all .DS_Store files and empty folders/subfolders within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        # Remove .DS_Store files
        for file_name in files:
            if file_name == '.DS_Store' or file_name == 'Thumbs.db' or file_name == '.picasa.ini':
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Removed .DS_Store file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        # Remove empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Now this check is more accurate post .DS_Store removal
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to remove {dir_path}: {e}")
    if not os.listdir(directory):  # Now this check is more accurate post .DS_Store removal
        try:
            os.rmdir(directory)
            print(f"Removed empty folder: {directory}")
        except Exception as e:
            print(f"Failed to remove {directory}: {e}")

def save_moved_files_log(log_path, moved_files):
    """Save a CSV log of moved files."""
    try:
        with open(log_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["MD5", "Original Path", "New Path"])
            for md5, orig_path, new_path in moved_files:
                writer.writerow([md5, orig_path, new_path])
        print(f"\nLog saved to: {log_path}")
    except Exception as e:
        print(f"Error writing log file: {e}")


def compute_md5(file_path, chunk_size=8192):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    return hash_md5.hexdigest()

def read_md5_hashes_from_csv(csv_path):
    md5_set = set()
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if "MD5 Checksum" not in reader.fieldnames:
                raise ValueError("CSV does not contain 'MD5 Checksum' column.")
            for row in reader:
                md5 = row["MD5 Checksum"].strip().lower()
                if md5:
                    md5_set.add(md5)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return md5_set

def move_file_preserve_structure(src_path, src_root, dst_root):
    """Move file while preserving relative folder structure."""
    relative_path = os.path.relpath(src_path, src_root)
    dst_path = os.path.join(dst_root, relative_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.move(src_path, dst_path)
    print(f"Moved: {src_path} -> {dst_path}")
    return dst_path

def search_and_move_matches(search_dir, known_md5s, dest_dir, recursive=True):
    moved_files = []
    for root, _, files in os.walk(search_dir):
        for name in files:
            full_path = os.path.join(root, name)
            file_md5 = compute_md5(full_path)
            if file_md5 and file_md5.lower() in known_md5s:
                new_path = move_file_preserve_structure(full_path, search_dir, dest_dir)
                moved_files.append((file_md5, full_path, new_path))
        if not recursive:
            break
    return moved_files

def main():
    parser = argparse.ArgumentParser(description="Move files matching MD5 hashes and log the results.")
    parser.add_argument("csv_file", help="Path to the CSV file containing MD5 hashes.")
    parser.add_argument("search_dir", help="Directory to search for matching files.")
    parser.add_argument("dest_dir", help="Destination directory to move matching files into.")
    # parser.add_argument("--log-file", default="moved_files_log.csv", help="Path to save the log CSV file.")
    # parser.add_argument("--no-recursive", action="store_true", help="Disable recursive directory search.")

    args = parser.parse_args()
    now = time.strftime("%y%m%d%H%M%S")
    # log_file = os.path.join(args.dest_dir,f"moved_files_log_{now}.csv")
    log_file = f"{args.dest_dir}_moved_files_log_{now}.csv"

    print("Reading known MD5 hashes...")
    known_md5s = read_md5_hashes_from_csv(args.csv_file)
    if not known_md5s:
        print("No valid MD5 hashes found. Exiting.")
        return

    print("Searching for matching files...")
    moved = search_and_move_matches(args.search_dir, known_md5s, args.dest_dir)

    if moved:
        print(f"\nMoved {len(moved)} matching file(s):")
        for md5, orig, new in moved:
            print(f"{md5} | {orig} -> {new}")
        save_moved_files_log(log_file, moved)
    else:
        print("No matching files found.")
    remove_empty_folders_and_ds_store(args.search_dir)


if __name__ == "__main__":
    main()