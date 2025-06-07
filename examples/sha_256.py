import os
import hashlib
from collections import defaultdict

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
    # Step 1: Group files by size
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                size = os.path.getsize(filepath)
                size_map[size].append(filepath)
            except OSError as e:
                print(f"Could not access {filepath}: {e}")

    # Step 2: For groups with same size, compare hashes
    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) < 2:
            continue  # No chance of duplicates
        for file in files:
            file_hash = hash_file(file)
            if file_hash:
                hash_map[file_hash].append(file)

    # Step 3: Return only duplicates
    duplicates = {hash_val: paths for hash_val, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def report_duplicates(duplicates):
    if not duplicates:
        print("No duplicate files found.")
        return

    print("\nDuplicate files found:")
    for i, (hash_val, files) in enumerate(duplicates.items(), 1):
        print(f"\nGroup {i} (Hash: {hash_val}):")
        for f in files:
            print(f"  - {f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python find_duplicates.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    duplicates = find_duplicates(target_dir)
    report_duplicates(duplicates)
