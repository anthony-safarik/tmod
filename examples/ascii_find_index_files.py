import os
import argparse

def find_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if filename == "file_index.txt":
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                print(f"{full_path}")
    return matches

def main():
    parser = argparse.ArgumentParser(description="find all file_index.txt")
    parser.add_argument("source", help="root Path to the file_index.txt")
    args = parser.parse_args()

    find_files(args.source)

if __name__ == "__main__":
    main()