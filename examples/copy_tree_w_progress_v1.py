#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def human_size(num):
    """Convert bytes to a human‑readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f}{unit}"
        num /= 1024
    return f"{num:.2f}PB"

def copy_tree_w_progress(src, dst, dry_run = False):
    """Copy files recursively from directory src to directory dst,
    skipping existing files and printing progress percentage after
    each successfully copied file.
    """

    # Collect all files to copy and total size
    files_to_copy = []
    total_size = 0

    for root, dirs, files in os.walk(src):
        dirs.sort()
        for f in sorted(files):
            full_src = os.path.join(root, f)
            size = os.path.getsize(full_src)
            total_size += size

            rel_path = os.path.relpath(full_src, src)
            full_dst = os.path.join(dst, rel_path)

            files_to_copy.append((full_src, full_dst, size))

    total_files = len(files_to_copy)
    copied_files = 0
    copied_size = 0

    for full_src, full_dst, size in files_to_copy:
        os.makedirs(os.path.dirname(full_dst), exist_ok=True)

        # Skip existing files
        if os.path.exists(full_dst):
            continue

        if not dry_run: shutil.copy2(full_src, full_dst)
        copied_files += 1
        copied_size += size

        # Progress calculations
        pct_files = (copied_files / total_files) * 100
        pct_size = (copied_size / total_size) * 100

        # Pretty output
        print(
            f"[{copied_files}/{total_files}] "
            f"{pct_files:6.2f}% files | {pct_size:6.2f}% data "
            f"({human_size(copied_size)} / {human_size(total_size)})\n"
            f"→ {full_src}"
        )

    print(f"Done. Dry run: {dry_run}")
