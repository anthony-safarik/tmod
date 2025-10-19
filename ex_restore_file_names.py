import os
import argparse
'''

/Volumes/X9Pro4TB/DATA/PHOTOS/2003/2003-08-15
/Volumes/X9Pro4TB/DATA/PHOTOS/2003/2003-08-24
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-05-01
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-05-02
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-06-19
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-07-24
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-07-25
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-07-31
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-07
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-10
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-13
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-14
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-17
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-27
/Volumes/X9Pro4TB/DATA/PHOTOS/2004/2004-08-28
/Volumes/X9Pro4TB/DATA/PHOTOS/2009/2009-04-05
/Volumes/X9Pro4TB/DATA/PHOTOS/2015/2015-03-12
/Volumes/X9Pro4TB/DATA/PHOTOS/2016/2016-11-12
/Volumes/X9Pro4TB/DATA/PHOTOS/2016/2016-12-08
/Volumes/X9Pro4TB/DATA/PHOTOS/2017/2017-09-23
/Volumes/X9Pro4TB/DATA/PHOTOS/2017/2017-10-29
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-05-21
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-06-24
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-06-27
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-07-01
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-07-03
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-07-05
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-07-12
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-07-17
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-09-22
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-10-19
/Volumes/X9Pro4TB/DATA/PHOTOS/2018/2018-12-23
/Volumes/X9Pro4TB/DATA/PHOTOS/2019/2019-03-01
/Volumes/X9Pro4TB/DATA/PHOTOS/2019/2019-08-18
/Volumes/X9Pro4TB/DATA/PHOTOS/2020/2020-09-09
/Volumes/X9Pro4TB/DATA/PHOTOS/2020/2020-11-25
/Volumes/X9Pro4TB/DATA/PHOTOS/2021/2021-07-17
/Volumes/X9Pro4TB/DATA/PHOTOS/2021/2021-10-11
/Volumes/X9Pro4TB/DATA/PHOTOS/2022/2022-04-17
/Volumes/X9Pro4TB/DATA/PHOTOS/2022/2022-04-18
'''



def restore_original_names(index_path="file_index.txt"):

    index_dirpath = os.path.dirname(index_path)

    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[1:]:  # Skip header
        parts = line.strip().split("\t")
        if len(parts) != 2:
            continue
        original, sanitized = parts

        original = os.path.join(index_dirpath,original)
        sanitized = os.path.join(index_dirpath,sanitized)

        if sanitized == original:
            continue
        if not os.path.exists(sanitized):
            print(f"❌ Missing sanitized file: {sanitized}")
            continue
        if os.path.exists(original):
            print(f"⚠️ Skipping: {original} already exists.")
            continue
        try:
            os.rename(sanitized, original)
            print(f"✅ Restored: {sanitized} -> {original}")
        except Exception as e:
            print(f"❌ Failed to restore {sanitized}: {e}")

def find_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if filename == "file_index.txt":
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                # print(f"{full_path}")
    return sorted(matches)

def main():
    parser = argparse.ArgumentParser(description="find all file_index.txt")
    parser.add_argument("source", help="root Path to the file_index.txt")
    args = parser.parse_args()

    files = find_files(args.source)
    for filename in files:
        filedir = os.path.dirname(filename)
        # null = input(filedir)
        restore_original_names(filename)

        desanitizer = os.path.join(filedir, "desanitizer.py")
        for item in (filename, desanitizer):
            if os.path.exists(item):
                print(f'removing - {item}')
                os.remove(item)


if __name__ == "__main__":
    main()