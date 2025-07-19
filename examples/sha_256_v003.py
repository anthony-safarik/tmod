import os
import hashlib
from collections import defaultdict
import shutil

LOG_FILE = "duplicate_report.txt"

def hash_file(filepath, block_size=65536):
    """Return SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None
    return hasher.hexdigest()

def find_duplicates(directory):
    size_map = defaultdict(list)

    # Step 1: Group by size (skip symlinks)
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.islink(filepath):
                continue  # Skip symlinks
            try:
                size = os.path.getsize(filepath)
                size_map[size].append(filepath)
            except OSError as e:
                print(f"Could not access {filepath}: {e}")

    # Step 2: Group by hash for files with same size
    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) < 2:
            continue
        for file in files:
            file_hash = hash_file(file)
            if file_hash:
                hash_map[file_hash].append(file)

    # Step 3: Only keep actual duplicates
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}

def report_duplicates(duplicates, log_path=LOG_FILE):
    with open(log_path, 'w') as log:
        if not duplicates:
            print("No duplicate files found.")
            log.write("No duplicate files found.\n")
            return

        print("\nDuplicate files found:")
        log.write("Duplicate files found:\n")

        for i, (hash_val, files) in enumerate(duplicates.items(), 1):
            print(f"\nGroup {i} (Hash: {hash_val}):")
            log.write(f"\nGroup {i} (Hash: {hash_val}):\n")
            for f in files:
                print(f"  - {f}")
                log.write(f"  - {f}\n")

def delete_duplicates(duplicates):
    print("\nWARNING: You're about to delete duplicate files (keeping only one per group).")
    confirm = input("Do you want to proceed? (y/N): ").lower()
    if confirm != 'y':
        print("Deletion canceled.")
        return

    for paths in duplicates.values():
        # Keep the first file, delete the rest
        for file_to_delete in paths[1:]:
            try:
                os.remove(file_to_delete)
                print(f"Deleted: {file_to_delete}")
            except Exception as e:
                print(f"Failed to delete {file_to_delete}: {e}")


def move_duplicates(duplicates, src_root, dest_root='duplicates'):
    print("\nWARNING: You're about to move out duplicate files (keeping only one per group).")
    confirm = input("Do you want to proceed? (y/N): ").lower()
    if confirm != 'y':
        print("Move canceled.")
        return

    for paths in duplicates.values():
        # Skip groups with less than 2 files
        if len(paths) < 2:
            continue

        for file_to_move in paths[1:]:  # Keep the first file, move the rest
            try:
                abs_path = os.path.abspath(file_to_move)
                relative_path = os.path.relpath(abs_path, start=src_root)
                dest_path = os.path.join(dest_root, relative_path)

                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                shutil.move(abs_path, dest_path)
                print(f"Moved: {file_to_move} -> {dest_path}")
            except Exception as e:
                print(f"Failed to move {file_to_move}: {e}")


if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Find duplicates in the source directory, keeping one of each group and moving the others to the destination directory.")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")
    args = parser.parse_args()

    src_dir = args.source
    dst_dir = args.destination

    if not os.path.isdir(src_dir):
        print(f"Error: '{src_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{src_dir}' for duplicate files...")
    duplicates = find_duplicates(src_dir)
    report_duplicates(duplicates)

    if duplicates:
        move_duplicates(duplicates, src_dir, dst_dir)
        print(f"\nReport saved to: {LOG_FILE}")
