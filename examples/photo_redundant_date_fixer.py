import os
import re

def remove_redundant_date_prefix_recursive(directory):
    # Match filenames starting with repeated YYYYMMDD, e.g., 20220321-20220321_anything.ext
    pattern = re.compile(r"^(?P<date>\d{8})-\1(?P<rest>.*)$")

    for root, _, files in os.walk(directory):
        for filename in files:
            match = pattern.match(filename)
            if match:
                new_filename = f"{match.group('date')}{match.group('rest')}"
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)

                if not os.path.exists(new_path):
                    print(f"Renaming: {old_path} → {new_path}")
                    os.rename(old_path, new_path)
                else:
                    print(f"Skipped (target exists): {new_path}")

if __name__ == "__main__":
    target_directory = input("Enter the directory to scan recursively: ").strip()
    if os.path.isdir(target_directory):
        remove_redundant_date_prefix_recursive(target_directory)
    else:
        print("Invalid directory.")

