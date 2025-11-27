#experiment in extracting md5 data from multiple csvs. running the file times how long it takes to save and load the data to various formats. pkl is factors faster

import csv, glob, os
import pickle, json

SRC = "/Volumes/SeaTopHat8TB/ARCHIVE/05_Archive"

def get_all_md5_from_manifest(csv_file):
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

def save_csv(data_set, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        for item in data_set:
            writer.writerow([item])

def save_txt(data_set,filepath):
    with open(filepath, "w") as f:
        for item in data_set:
            f.write(str(item) + "\n")

def load_txt(filepath):
    """
    Reads a text file and returns its lines as a list.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Strip newline characters for cleaner output
    return [line.strip() for line in lines]

def save_json(data_set, filepath):
    # Convert set to list (JSON doesn’t support sets directly)
    with open(filepath, "w") as f:
        json.dump(list(data_set), f)

def load_json(filepath):
    # Load it back
    with open(filepath, "r") as f:
        loaded_set = set(json.load(f))
    return loaded_set

manifest_file_paths = glob.glob(f'{SRC}/*/file_manifest.csv')

def get_md5_set_from_manifests(list_of_manifest_filepaths):
    combined_list = []
    for manifest_file in list_of_manifest_filepaths:
        md5_list = get_all_md5_from_manifest(manifest_file)
        combined_list = combined_list + md5_list
    return set(combined_list)

if __name__ == "__main__":
    from timeit import time_it

    @time_it
    def time_csv_read():
        return get_md5_set_from_manifests(manifest_file_paths)

    @time_it
    def time_save_and_load_csv(m,f="md5_set.txt"):
        save_csv(m,f)
        data = set(load_txt(f))
        print(f'time_save_and_load_csv --- loaded data matches saved: {data == m}')
        os.remove("md5_set.txt")

    @time_it
    def time_save_and_load_pkl(m,f="md5_set.pkl"):
        save_pkl(m,f)
        data = load_pkl(f)
        print(f'time_save_and_load_pkl --- loaded data matches saved: {data == m}')
        os.remove("md5_set.pkl")

    @time_it
    def time_save_and_load_json(m,f="md5_set.json"):
        save_json(m,f)
        data = load_json(f)
        print(f'time_save_and_load_json --- loaded data matches saved: {data == m}')
        os.remove("md5_set.json")

    all_md5 = time_csv_read()
    print (len(all_md5))
    time_save_and_load_csv(all_md5)
    time_save_and_load_pkl(all_md5)
    time_save_and_load_json(all_md5)
