import os
import re
import shutil
from datetime import datetime

def organize_pxl_files(base_dir):
    # Matches filenames like: 20221119-PXL_20221120_012919290.MP.jpg
    pattern = re.compile(r"^(?P<outer>\d{8})-PXL_(?P<inner>\d{8})_(?P<rest>.+)$")

    for root, _, files in os.walk(base_dir):
        for file in files:
            match = pattern.match(file)
            if match:
                outer_date = match.group('outer')
                inner_date = match.group('inner')
                rest = match.group('rest')
                
                # New filename: PXL_<inner>_<rest>
                new_filename = f"PXL_{inner_date}_{rest}"

                # New destination path: base/YYYY/YYYY-MM-DD/
                dt = datetime.strptime(inner_date, "%Y%m%d")
                yyyy = dt.strftime("%Y")
                yyyy_mm_dd = dt.strftime("%Y-%m-%d")
                new_dir = os.path.join(base_dir, yyyy, yyyy_mm_dd)
                os.makedirs(new_dir, exist_ok=True)

                old_path = os.path.join(root, file)
                new_path = os.path.join(new_dir, new_filename)

                if not os.path.exists(new_path):
                    print(f"Moving: {old_path} → {new_path}")
                    shutil.move(old_path, new_path)
                else:
                    print(f"Skipped (target exists): {new_path}")

if __name__ == "__main__":
    base_directory = input("Enter the base directory to scan: ").strip()
    if os.path.isdir(base_directory):
        organize_pxl_files(base_directory)
    else:
        print("Invalid directory.")
