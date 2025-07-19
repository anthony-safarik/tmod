import os
import argparse
import re

def contains_non_ascii(text):
    """Check if text contains any non-ASCII characters."""
    try:
        text.encode('ascii')
        return False
    except UnicodeEncodeError:
        return True

def is_unclean(name):
    # Separate name and extension
    base, ext = os.path.splitext(name)
    # Romanize (convert to ASCII)
    base_ascii = base.encode('ascii', 'ignore').decode('ascii') or "RENAME_ME"
    # Remove non-alphanumeric characters
    base_clean = re.sub(r'[^A-Za-z0-9\-_.]', '', base_ascii)
    # 
    clean_name = f"{base_clean}{ext}"
    if clean_name == name:
        return False
    elif clean_name != name:
        print('________')
        print(name)
        print(clean_name)
        return True

def find_folders_with_non_ascii_files(root_dir):
    folders_with_non_ascii = set()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # if contains_non_ascii(filename):
            if is_unclean(filename):
                folders_with_non_ascii.add(dirpath)
                # print(dirpath)
                break  # No need to check more files in this folder

    return folders_with_non_ascii

def main():
    parser = argparse.ArgumentParser(description="Report ascii folders")
    parser.add_argument("source", help="Path to the root folder")
    args = parser.parse_args()
    folders = find_folders_with_non_ascii_files(args.source)
    for folder in folders:
        # pass
        print(folder)
    print(f'{len(folders)} folders have non standard characters')

if __name__ == "__main__":
    main()
