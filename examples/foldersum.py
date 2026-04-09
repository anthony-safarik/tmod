# -*- coding: utf-8 -*-

import os

def get_summary(paths):
    total_size = 0
    for i, path in enumerate(paths, 1):
        total_size += os.path.getsize(path)
    print(f"file count: {i}\nbytes: {total_size}\ntotal size GB: {total_size / (1000**3):.2f}GB")

    size_gb = total_size / (1000**3)
    size_gb = round(size_gb,2)

    summary = {
    "File Count": i,
    "Total Size": total_size,
    "Total Size GB": size_gb
    }

    return summary