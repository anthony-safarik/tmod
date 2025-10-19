#danger, don't run this twice or you will lose reference to original file names

import argparse

from examples.ascii_report import find_folders_with_non_ascii_files
from examples.ascii_index_maker_v1 import make_file_index
from examples.ascii_sanitizer_v1 import rename_from_index
from examples.ascii_create_desanitizer import create_desanitizer

def main():
    parser = argparse.ArgumentParser(description="Create file index with sanitized names for each folder and rename")
    parser.add_argument("source", help="Path to the root folder")
    args = parser.parse_args()
    folders = find_folders_with_non_ascii_files(args.source)
    for folder in folders:
        print(folder)
        file_index = make_file_index(folder)
        rename_from_index(file_index)
        create_desanitizer(folder)



    print(f'{len(folders)} folders have non standard characters')

if __name__ == "__main__":
    main()