import os
import argparse

LOG_FILE = "yi4k_renames.csv"

def find_y_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            hyphen_split = name.split('-')
            if len(hyphen_split) == 2:
                print(hyphen_split)
                # if hyphen_split[1].startswith("Y") and len(name) == 8:
                if hyphen_split[1].startswith("Y") and len(name) == 17:
                    full_path = os.path.join(root, filename)
                    matches.append(full_path)
                    # print(f"Match: {full_path}")
    return matches

# def report_renames(duplicates, log_path=LOG_FILE):
#         if not duplicates:
#             print("No duplicate files found.")
#             log.write("No duplicate files found.\n")
#             return

#         print("\nDuplicate files found:")
#         log.write("Duplicate files found:\n")

#         for i, (hash_val, files) in enumerate(duplicates.items(), 1):
#             print(f"\nGroup {i} (Hash: {hash_val}):")
#             log.write(f"\nGroup {i} (Hash: {hash_val}):\n")
#             for f in files:
#                 print(f"  - {f}")
#                 log.write(f"  - {f}\n")

def main():
    parser = argparse.ArgumentParser(description="Find files that start with 'Y' and are 8 characters long.")
    parser.add_argument("directory", help="Directory to search")
    parser.add_argument("target", help="Path to the target directory")
    args = parser.parse_args()

    matches = find_y_files(args.directory)

    with open(LOG_FILE, 'w') as log:
        log.write("Source Path, Target Path\n")

        for match in matches:
            # Compute relative path from src root
            rel_path = os.path.relpath(match, args.directory)
            alt_filename = os.path.basename(rel_path).split('-')[1]
            alt_rel_path = os.path.join(os.path.dirname(rel_path), alt_filename)
            target_path = os.path.join(args.target, alt_rel_path)
            print(rel_path, target_path)
            log.write(f"{match}, {target_path}\n")

            target_dir = os.path.dirname(target_path)
            os.makedirs(target_dir, exist_ok=True)
            os.rename(match, target_path)
        

if __name__ == "__main__":
    main()
