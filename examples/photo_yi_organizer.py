import os
import argparse

def find_y_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            # if name.startswith("Y") and len(name) == 8:
            if name.startswith("Y"):
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                # print(f"Match: {full_path}")
    return matches

def main():
    parser = argparse.ArgumentParser(description="Find files that start with 'Y' and are 8 characters long.")
    parser.add_argument("directory", help="Directory to search")
    parser.add_argument("target", help="Path to the target directory")
    args = parser.parse_args()

    matches = find_y_files(args.directory)

    for match in matches:
        # Compute relative path from src root
        rel_path = os.path.relpath(match, args.directory)
        target_path = os.path.join(args.target, rel_path)
        print(rel_path, target_path)

        target_dir = os.path.dirname(target_path)
        # os.makedirs(target_dir, exist_ok=True)
        # os.rename(match, target_path)
        

if __name__ == "__main__":
    main()
