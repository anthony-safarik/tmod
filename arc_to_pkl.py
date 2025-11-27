#experiment in extracting md5 data from multiple csvs. running the file times how long it takes to save and load the data to various formats. pkl is factors faster

import csv, glob, os
import pickle, json

SRC = "/srv/dev-disk-by-uuid-68ba9fa2-5f0f-4c10-bd06-5afb9814ae22/archive_buckets"
SRC = "/Volumes/archive_buckets"
DST = "/Volumes/data_share/test/md5_set.pkl"


manifest_file_paths = glob.glob(f'{SRC}/*/file_manifest.csv')

def get_md5_from_manifest(csv_file):
    """
    Params: path to file_manifest.csv
    Returns list of MD5)
    """
    results = []

    with open(csv_file, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            _, _, csv_md5, _ = row
            results.append((csv_md5))

    return results

def save_pkl(data, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(data, f)

def load_pkl(filepath):
    with open(filepath, "rb") as f:
        loaded_data = pickle.load(f)
    return loaded_data

def index_all_md5(list_of_manifest_filepaths):
    combined_list = []
    for manifest_file in list_of_manifest_filepaths:
        md5_list = get_md5_from_manifest(manifest_file)
        combined_list = combined_list + md5_list
    return set(combined_list)

if __name__ == "__main__":
    md5_set = index_all_md5(manifest_file_paths)
    save_pkl(md5_set,DST)
