import os
import argparse
import re
\

def sanitize_filename(name):
    # Separate name and extension
    base, ext = os.path.splitext(name)
    # Romanize (convert to ASCII)
    base_ascii = base.encode('ascii', 'ignore').decode('ascii') or "RENAME_ME"
    # Remove non-alphanumeric characters
    base_clean = re.sub(r'[^A-Za-z0-9\-_]', '', base_ascii)
    # Return the cleaned filename with the original extension
    return f"{base_clean}{ext.lower()}"

def make_file_index(folder_path):
    file_index = os.path.join(folder_path,"file_index.txt")

    file_list = []

    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path,fname)
        if os.path.isfile(fpath):
            #   file_list.append(fpath)
              file_list.append(fname)

    formatted_list = []
    counter = 1
    with open(file_index, "w", encoding="utf-8") as textfile:
        # write the header
        textfile.write(f"Original\tSanitized\n")
        for f in sorted(file_list):
            name = os.path.basename(f)
            dir = os.path.dirname(f)
            formatted = sanitize_filename(name)
            if formatted in formatted_list:
                base, ext = os.path.splitext(formatted)
                formatted = base+'_'+str(counter)+ext
            formatted_list.append(formatted)
            print(f, formatted)
            counter += 1
            # textfile.write(f"{f}\t{os.path.join(folder_path,formatted)}\n")
            textfile.write(f"{f}\t{formatted}\n")

def main():
    parser = argparse.ArgumentParser(description="Create an ascii file index.")
    parser.add_argument("source", help="Path to the source directory")
    args = parser.parse_args()

    make_file_index(args.source)

if __name__ == "__main__":
    main()