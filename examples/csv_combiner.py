import os
import csv

def gen_csv_files(directory):
    """Recursively yields csv files within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(root, file_name)
                yield file_path

def combine_csv_files(folder_path, output_file):
    # Find all .csv files in the folder
    csv_generator = gen_csv_files(folder_path)
    csv_files = [f for f in csv_generator]

    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Open output file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = None

        for filename in csv_files:
            file_path = os.path.join(folder_path, filename)
            print(f"Reading: {file_path}")

            with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)

                # Write header only once
                if writer is None:
                    writer = csv.writer(outfile)
                    writer.writerow(header)

                # Write the rest of the data
                for row in reader:
                    writer.writerow(row)

    print(f"\nCombined {len(csv_files)} files into: {output_file}")

# === USAGE EXAMPLE ===
# Replace with your actual folder path and output file name
folder = '/Volumes/X9Pro4TB/DATA/Archive'
output = '/Volumes/X9Pro4TB/DATA/archive.csv'

combine_csv_files(folder, output)
