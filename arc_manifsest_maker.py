import os, csv, hashlib
from datetime import datetime

def calculate_md5(file_path, block_size=65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()

def get_file_info(file_path, folder_path):
    file_size = os.path.getsize(file_path)
    file_md5 = calculate_md5(file_path)
    file_timestamp = os.path.getmtime(file_path)
    timestamp_str = datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    relative_path = os.path.relpath(file_path, folder_path)
    return relative_path, file_size, file_md5, timestamp_str

def generate_file_manifest(path_to_assets_folder):
    """
    creates a file_manifest.csv in the parent dir

    Params:
        path_to_assets_folder: file contents
    """
    parent_directory = os.path.dirname(path_to_assets_folder)
    output_csv = os.path.join(parent_directory, 'file_manifest.csv')
    
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Path', 'Bytes', 'MD5', 'Timestamp'])

        for dirpath, dirnames, filenames in os.walk(path_to_assets_folder):
            for filename in filenames:
                if not filename.startswith('.'):
                    file_path = os.path.join(dirpath, filename)
                    file_info = get_file_info(file_path, path_to_assets_folder)
                    csv_writer.writerow(file_info)

if __name__ == "__main__":
     SRC = "/Users/tonysafarik/_scratch/_Test/assets"
     SRC = "/Volumes/ORICO/OFFLOADS"
     generate_file_manifest(SRC)