import hashlib
import time
import sys
import os

def calculate_hashes(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    # Define chunk size for reading file in blocks
    chunk_size = 8192

    # Calculate SHA-256
    sha256_hash = hashlib.sha256()
    start_sha256 = time.time()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256_hash.update(chunk)
    end_sha256 = time.time()
    sha256_digest = sha256_hash.hexdigest()
    sha256_time = end_sha256 - start_sha256

    # Calculate MD5
    md5_hash = hashlib.md5()
    start_md5 = time.time()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5_hash.update(chunk)
    end_md5 = time.time()
    md5_digest = md5_hash.hexdigest()
    md5_time = end_md5 - start_md5

    # Print results
    print(f"SHA-256: {sha256_digest}")
    print(f"Time taken for SHA-256: {sha256_time:.6f} seconds")
    print(f"MD5:     {md5_digest}")
    print(f"Time taken for MD5:     {md5_time:.6f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hash_calc.py <file_path>")
    else:
        calculate_hashes(sys.argv[1])
