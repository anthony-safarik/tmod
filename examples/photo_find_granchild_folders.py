import os

def find_grandchildren_with_folders(root_dir):
    results = []

    for child in os.listdir(root_dir):
        child_path = os.path.join(root_dir, child)
        if not os.path.isdir(child_path):
            continue

        for grandchild in os.listdir(child_path):
            grandchild_path = os.path.join(child_path, grandchild)
            if not os.path.isdir(grandchild_path):
                continue

            # Check if the grandchild folder contains any directories
            subdirs = [entry for entry in os.listdir(grandchild_path)
                       if os.path.isdir(os.path.join(grandchild_path, entry))]

            if subdirs:
                results.append(grandchild_path)
                print(f"Grandchild folder with subfolders: {grandchild_path}")

    return results

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find grandchildren folders that contain folders.")
    parser.add_argument("root_dir", help="Root directory to search.")
    args = parser.parse_args()

    matches = find_grandchildren_with_folders(args.root_dir)
    print(f"\nTotal matches: {len(matches)}")
