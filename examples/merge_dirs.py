import os
import shutil

def merge_directories(src, dst):
    if not os.path.isdir(src):
        print(f"Source directory '{src}' does not exist.")
        return
    if not os.path.isdir(dst):
        os.makedirs(dst, exist_ok=True)

    for root, dirs, files in os.walk(src, topdown=False):
        # Compute relative path from src root
        rel_path = os.path.relpath(root, src)
        dst_dir = os.path.join(dst, rel_path)

        # Ensure destination subdirectory exists
        os.makedirs(dst_dir, exist_ok=True)

        # Move files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, file)

            if os.path.exists(dst_file):
                print(f"Skipping file (already exists): {dst_file}")
                continue

            # shutil.move(src_file, dst_file)
            os.rename(src_file, dst_file)
            print(f"Moved: {src_file} -> {dst_file}")

        # After moving files, remove empty directory if it's now empty
        if not os.listdir(root):
            os.rmdir(root)
            print(f"Removed empty directory: {root}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Merge two directories, skipping file collisions and cleaning up.")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")
    args = parser.parse_args()

    merge_directories(args.source, args.destination)
