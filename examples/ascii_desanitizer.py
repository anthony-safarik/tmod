import os
import argparse

def restore_original_names(index_path="file_index.txt"):
    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[1:]:  # Skip header
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue
        original, sanitized = parts
        if sanitized == original:
            continue
        if not os.path.exists(sanitized):
            print(f"❌ Missing sanitized file: {sanitized}")
            continue
        if os.path.exists(original):
            print(f"⚠️ Skipping: {original} already exists.")
            continue
        try:
            os.rename(sanitized, original)
            print(f"✅ Restored: {sanitized} -> {original}")
        except Exception as e:
            print(f"❌ Failed to restore {sanitized}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename files based on file_index.txt")
    parser.add_argument("source", help="Path to the file_index.txt")
    args = parser.parse_args()

    restore_original_names(args.source)

if __name__ == "__main__":
    main()