'''
this script accepts a folder full of archived blurays 
(or any folder that matches the pattern chunk-subfolder/file_manifest.csv) and reads the csv files.
It writes out new csv files in chunks determined by the global variable and skips duplicates 
which are written to a "duplicates" csv file.
The idea is to break the big subfolder of assets into chunks and another script could pick these up and Process
into real, packed archive folder.
for example, scattered photos on different hard disks could be added to an assets folder, a csv is created,
then the master folder is copied to a master disk where the chunker is applied
files are packed into archive chunks, duplicates are culled
packed archive chunks are passed through verification (and ultimately backup + verification)and then
all the md5 for all the files are added to the "truth table"

TO DO:
add functionality to the group files function to read in the truth table and use the existing md5 to allow for filtering 
out duplicates within the larger set of archive chunks
consider adding the original master asset subfolder to the resulting CSVs. maybe just the duplicates?
The question is what is the value of maintaining these original sets? 
is it better just to backup everything? 
is it better to preserve just one copy?
how and when would you want to reconstruct the original folder?
'''

import csv
import glob
import time
import os
# import sys
NOW = time.strftime("%y%m%d%H%M%S")
OUTPUT_DIR = os.path.join("/Users/tonysafarik/_scratch", f'{NOW}_csv_chunked')
CHUNK_SIZE = 50 * 1000**3  # 50 GB in bytes
CHUNK_PREFIX = "BDL-"

def group_files(csv_files):
    seen_md5 = set()
    duplicates = []
    chunks = []
    current_chunk = []
    current_size = 0

    for csv_file in csv_files:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                file_path = row["File Path"]
                size = int(row["Bytes"])
                md5 = row["MD5"]
                timestamp = row["Timestamp"]

                # Check for duplicates
                if md5 in seen_md5:
                    duplicates.append(row)
                    continue
                seen_md5.add(md5)

                # If adding this file exceeds 50GB, start a new chunk
                if current_size + size > CHUNK_SIZE:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_size = 0

                current_chunk.append(row)
                current_size += size

    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks, duplicates

def write_chunks(chunks, duplicates):
    # Make output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Write chunks to separate CSV files
    for i, chunk in enumerate(chunks, 1):
        filename = f"{OUTPUT_DIR}/{CHUNK_PREFIX}{str(i).zfill(4)}.csv"
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["File Path", "Bytes", "MD5", "Timestamp"])
            writer.writeheader()
            writer.writerows(chunk)
        print(f"Written {len(chunk)} files to {filename}")

    # Write duplicates to a separate file
    if duplicates:
        with open(f"{OUTPUT_DIR}/duplicates_{NOW}.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["File Path", "Bytes", "MD5", "Timestamp"])
            writer.writeheader()
            writer.writerows(duplicates)
        print(f"Written {len(duplicates)} duplicate files to duplicates.csv")

def main():
    # if len(sys.argv) < 2:
    #     print("Usage: python group_files.py <input1.csv> <input2.csv> ...")
    #     sys.exit(1)

    # csv_files = sys.argv[1:]
    csv_files = sorted(glob.glob("/Volumes/archive_buckets/*/file_manifest.csv"))
    chunks, duplicates = group_files(csv_files)
    write_chunks(chunks, duplicates)

    # Print summary
    for i, chunk in enumerate(chunks, 1):
        total_size = sum(int(file["Bytes"]) for file in chunk)
        print(f"Chunk {i}: {len(chunk)} files, {total_size / (1000**3):.2f} GB")

if __name__ == "__main__":
    main()
