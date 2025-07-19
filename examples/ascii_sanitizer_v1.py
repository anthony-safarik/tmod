import os
import argparse

def rename_from_index(index_path="file_index.txt"):

    index_dirpath = os.path.dirname(index_path)

    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip the header
    for line in lines[1:]:
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue
        original, sanitized = parts

        original = os.path.join(index_dirpath,original)
        sanitized = os.path.join(index_dirpath,sanitized)
        
        if original == sanitized:
            continue
        if not os.path.exists(original):
            print(f"❌ File not found: {original}")
            continue
        if os.path.exists(sanitized):
            print(f"⚠️ Skipping: {sanitized} already exists.")
            continue
        try:
            os.rename(original, sanitized)
            print(f"✅ Renamed: {original} -> {sanitized}")
        except Exception as e:
            print(f"❌ Failed to rename {original}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename files based on file_index.txt")
    parser.add_argument("source", help="Path to the file_index.txt")
    args = parser.parse_args()

    rename_from_index(args.source)

if __name__ == "__main__":
    main()