import os
import hashlib
from collections import defaultdict

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python find_duplicates.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{target_dir}' for duplicate files...")

    duplicates = find_duplicates(target_dir)
    report_duplicates(duplicates)

    if duplicates:
        delete_duplicates(duplicates)
        print(f"\nReport saved to: {LOG_FILE}")
