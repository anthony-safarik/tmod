import pickle, csv

manifest = "/Users/tonysafarik/_scratch/_Test/file_manifest.csv"

def load_pkl(filepath):
    with open(filepath, "rb") as f:
        loaded_data = pickle.load(f)
    return loaded_data

def find_matching_md5(csv_file, md5_set):
    """
    Params: path to file_manifest.csv, set of md5 to reference
    """
    results_redundant = []
    results_unique = []

    with open(csv_file, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            _, _, csv_md5, _ = row
            if csv_md5 in md5_set:
                results_redundant.append(row)
            else:
                results_unique.append(row)

    return results_redundant, results_unique

def write_csv(csv_file_path, rows):
    """
    creates a file_manifest.csv
    Params: path to the csv to write, rows to write
    """

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File Path', 'Bytes', 'MD5', 'Timestamp'])
        for row in rows:
            csv_writer.writerow(row)

redundant_rows, unique_rows = find_matching_md5(manifest, load_pkl("/Volumes/data_share/test/md5_set.pkl"))
write_csv("/Users/tonysafarik/_scratch/_Test/file_manifest_unique.csv", unique_rows)
write_csv("/Users/tonysafarik/_scratch/_Test/file_manifest_redundant.csv", redundant_rows)