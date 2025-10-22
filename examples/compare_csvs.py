import csv
import os

def get_csv_data(file_path):
    """
    Reads a CSV file and returns the header and list of rows (as dictionaries).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        return reader.fieldnames, rows

def write_csv_data(file_path, fieldnames, rows):
    if file_path:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in rows:
                print(row)
                writer.writerow(row)

def main():
    print("=== CSV Comparison Tool ===")
    file1_path = input("Enter path to first (file to check) CSV file: ").strip()
    file2_path = input("Enter path to second (reference) CSV file: ").strip()
    unmatched_output_csv_path = input("Optionally Enter path to output UNMATCHED to CSV file: ").strip()
    matched_output_csv_path = input("Optionally Enter path to output MATCHED to CSV file: ").strip()

    try:
        header1, rows1 = get_csv_data(file1_path)
        header2, rows2 = get_csv_data(file2_path)
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    print("\nColumns in first file:", header1)
    column_to_compare = input("Enter column name to compare: ").strip()

    if column_to_compare not in header1 or column_to_compare not in header2:
        print(f"Error: Column '{column_to_compare}' not found in both files.")
        return

    # Extract set of values from column in file 2 for fast lookup
    file2_values = {row[column_to_compare] for row in rows2}

    # Compare and collect unmatched rows from file 1
    unmatched_rows = [row for row in rows1 if row[column_to_compare] not in file2_values]
    matched_rows = [row for row in rows1 if row[column_to_compare] in file2_values]

    print(f"\n=== Unmatched rows in '{file1_path}' based on column '{column_to_compare}' ===")
    if unmatched_rows:
        for row in unmatched_rows:
            print(row)
        print(f"\nTotal unmatched rows: {len(unmatched_rows)}")
        write_csv_data(unmatched_output_csv_path, header1, unmatched_rows)
        write_csv_data(matched_output_csv_path, header1, matched_rows)
    else:
        print("All rows in the first file have a match in the second file based on the specified column.")

if __name__ == "__main__":
    main()
