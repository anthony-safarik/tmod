# move files in SRC existing in REF to DST

import os
from pathlib import Path

def gen_paths(input_path):
    """
    Walk through the directory and generate Posix paths for files.
    """
    if os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            dirs.sort()
            for file_name in sorted(files):
                if not file_name.startswith("."):
                    yield Path(root) / file_name

def hyper_gen_relpaths(path_iterable, other_path):
    """
    Turn a path iterable into relative paths
    """
    for i in path_iterable:
        yield Path.relative_to(i,other_path)

def rename_file_path(relpath,src,dst):
        
        source_file_full_path = src / relpath
        moved_file_full_path = dst / relpath
        moved_file_parent = moved_file_full_path.parent

        os.makedirs(str(moved_file_parent), exist_ok=True)
        print (f"moving {source_file_full_path}")
        os.rename(str(source_file_full_path), str(moved_file_full_path))

def main(src, ref, dst):
    paths_list = [i for i in hyper_gen_relpaths((gen_paths(ref)),ref)]
    for relpath in hyper_gen_relpaths(gen_paths(src),src):
        if relpath in paths_list:
            rename_file_path(relpath,src,dst)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="move source files existing in reference to destination")
    parser.add_argument("src", help="source file directory")
    parser.add_argument("ref", help="reference directory")
    parser.add_argument("dst", help="destination file directory")
    args = parser.parse_args()

    main(args.src, args.ref, args.dst)