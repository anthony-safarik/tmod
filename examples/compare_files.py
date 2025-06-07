import os
import filecmp

def compare_dirs(dir1, dir2):
    print(f"Comparing directories:\n - {dir1}\n - {dir2}\n")
    # Perform a shallow comparison
    comparison = filecmp.dircmp(dir1, dir2)

    # Report differences
    report_differences(comparison)

def report_differences(comparison, indent=0):
    prefix = " " * indent
    if comparison.left_only:
        print(f"{prefix}Only in {comparison.left}: {comparison.left_only}")
    if comparison.right_only:
        print(f"{prefix}Only in {comparison.right}: {comparison.right_only}")
    if comparison.diff_files:
        print(f"{prefix}Differing files: {comparison.diff_files}")
    if comparison.funny_files:
        print(f"{prefix}Trouble comparing: {comparison.funny_files}")

    # Recurse into subdirectories
    for subdir in comparison.subdirs:
        # print(f"\n{prefix}Subdirectory: {subdir}")
        report_differences(comparison.subdirs[subdir], indent + 4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compare two directories and report differences.")
    parser.add_argument("dir1", help="First directory path")
    parser.add_argument("dir2", help="Second directory path")
    args = parser.parse_args()

    if not os.path.isdir(args.dir1) or not os.path.isdir(args.dir2):
        print("Both arguments must be valid directories.")
    else:
        compare_dirs(args.dir1, args.dir2)
