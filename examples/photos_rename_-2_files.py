import os
import re

def rename_files_with_suffix(root_dir, suffix='-2'):
    pattern = re.compile(rf"^(.*){re.escape(suffix)}(\.[^.]+)$")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            match = pattern.match(filename)
            if match:
                original_name = match.group(1) + match.group(2)
                src_path = os.path.join(dirpath, filename)
                dst_path = os.path.join(dirpath, original_name)

                # Avoid overwriting existing files
                if os.path.exists(dst_path):
                    print(f"Skipping: {dst_path} already exists.")
                    continue

                os.rename(src_path, dst_path)
                # print(f"Renamed: {filename} -> {original_name}")
                print(f"Renamed: {src_path} -> {dst_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rename files ending with -2 before extension.")
    parser.add_argument("root_dir", help="Root directory to search and rename files.")
    args = parser.parse_args()

    rename_files_with_suffix(args.root_dir)
