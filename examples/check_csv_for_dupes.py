import csv
import hashlib
import os

def load_multiple_csv(csv_filenames):
    """Load data from multiple CSV files and combine them into one list."""
    file_data = []
    for csv_filename in csv_filenames:
        with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                file_data.append({
                    'File Path': row['File Path'],
                    'Bytes': int(row['Bytes']),
                    'MD5': row['MD5'],
                    'Timestamp': row['Timestamp']
                })
    return file_data

def compute_md5(file_path):
    """Compute the MD5 hash of a file."""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def check_duplicate(csv_filenames, files_to_check):
    """Check multiple files for duplicates across multiple CSVs."""
    # Load CSV data from all files
    csv_data = load_multiple_csv(csv_filenames)

    # Create a set of MD5 hashes from the combined CSV data for faster lookup
    csv_md5_hashes = {entry['MD5']: entry for entry in csv_data}

    # Iterate over the list of files to check
    for file_to_check in files_to_check:
        print(f"Checking file: {file_to_check}")
        file_md5 = compute_md5(file_to_check)
        
        if file_md5 is None:
            print(f"Skipping {file_to_check} due to error (file not found).")
            continue

        # Check if the file's MD5 is in the CSV MD5 hashes set
        if file_md5 in csv_md5_hashes:
            duplicate_entry = csv_md5_hashes[file_md5]
            print(f"Duplicate found for {file_to_check}:")
            print(f"  Matching file: {duplicate_entry['File Path']}")
            print(f"  MD5: {duplicate_entry['MD5']}")
            print(f"  Timestamp: {duplicate_entry['Timestamp']}")
        else:
            print(f"No duplicate found for {file_to_check}.")



def crawl_dir(inpath,file_ending=''):
    '''
    inpath is a string representing a DIRECTORY on the file system
    file_ending is a string matching end of file name
    returns a sorted list of files from inpath
    '''
    filepath_list=[]
    for (path,dirs,files) in os.walk(inpath):
        for item in files:
            if item.endswith(file_ending):
                filepath = os.path.join(path,item)
                if filepath not in filepath_list:
                    filepath_list.append(filepath)
    return sorted(filepath_list)

# Example usage
# csv_file = '/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0043/file_manifest.csv'  # Path to your CSV file

# Example usage
csv_files = ['/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0043/file_manifest.csv', '/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0042/file_manifest.csv', '/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0041/file_manifest.csv']  # List of multiple CSV files
files_to_check = crawl_dir('/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive/BDR-0043/assets/PHOTOS/2017', '.JPG')
# files_to_check = [
#     'PHOTOS/2017/2017-05-13/DSC03570.dng',  # List of files you want to check
#     'PHOTOS/2017/2017-05-13/DSC03571.dng',
#     'PHOTOS/2017/2017-05-13/DSC03571.JPG',
#     'PHOTOS/2017/2017-05-13/DSC03572.dng'
# ]

check_duplicate(csv_files, files_to_check)