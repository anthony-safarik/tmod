#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def copy_tree_w_progress(src, dst):
    """Copy files recursively from directory src to directory dst,
    skipping existing files and printing progress percentage after
    each successfully copied file.
    """

    # Collect all files to copy and get total size
    files_to_copy = []
    total_size = 0
    for root, dirs, files in os.walk(src):
        for f in files:
            full_src = os.path.join(root, f)
            total_size += os.path.getsize(full_src)
            rel_path = os.path.relpath(full_src, src)
            full_dst = os.path.join(dst, rel_path)
            files_to_copy.append((full_src, full_dst))

    total = len(files_to_copy)
    copied = 0
    copied_size = 0

    for full_src, full_dst in files_to_copy:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(full_dst), exist_ok=True)

        # Skip if file already exists
        if os.path.exists(full_dst):
            continue

        # Copy file
        shutil.copy2(full_src, full_dst)
        copied += 1
        copied_size += os.path.getsize(full_src)

        # Print progress
        progress_files_copied = (copied / total) * 100
        progress_data_copied = (copied_size / total_size) * 100
        print(f"Copying {full_src}\nfiles copied: {progress_files_copied:.2f}%... data copied {progress_data_copied:.2f}%")
        #TODO make this prettier and add "file x of total number of files"

    print("Done.")


# def merge_files_with_status(src, dst, operation = 'copy'):
#     """Copy files from source folder to destination folder."""
#     total_size, total_count = HashPack.get_folder_size_and_file_count(src)
#     cumulative_size = 0
#     cumulative_count = 0
#     for (path, dirs, files) in os.walk(src):
#         for item in files:
#             cumulative_count += 1
#             src_file_path = os.path.join(path, item)
#             dst_folder_path = path.replace(src,dst)
#             dst_file_path = os.path.join(dst_folder_path,item)
#             src_file_size = os.path.getsize(src_file_path)
#             cumulative_size += src_file_size
#             print(f"\nCopying file {cumulative_count} of {total_count}... \n     {item}")
#             if not os.path.exists(dst_folder_path): os.makedirs(dst_folder_path)
#             if not os.path.exists(dst_file_path): HashPack.copy_file(src_file_path, dst_file_path)
#             print(f"     {cumulative_size} of {total_size} bytes copied ({str(100 * float(cumulative_size)/float(total_size)).split('.')[0]}% of {total_size/1e+9} GB)\n")
#             if os.path.exists(dst_file_path) and os.path.getsize(dst_file_path) == src_file_size:
#                 print('File size matches')
#                 if operation == 'move':
#                     os.remove(src_file_path)
#                     if len(os.listdir(path)) == 0:
#                         os.rmdir(path)
#     dst_total_size, dst_total_count = HashPack.get_folder_size_and_file_count(dst)
#     if total_size == dst_total_size and total_count == dst_total_count:
#         print("Source and destination folders match")
#     else:
#         print(f"Source and destination folders don't match\n     {src}\n     {total_count, total_size}\n     {dst}\n     {total_count, total_size}")
#     if operation == 'move':
#         HashPack.delete_empty_folders(src)