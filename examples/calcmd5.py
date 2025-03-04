import hashlib
import os # to remove file

def calc_md5(file_path):
    """Calculate the MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

if __name__ == "__main__":
    # Make temp file
    with open('tempfile.txt', 'w') as file:
        # Write some sample text
        file.write('Temp File')

    md5 = calc_md5("tempfile.txt")
    os.remove('tempfile.txt')

    assert md5 == "0af95f183bd6cc7c6ae3022c9cf6f879"
    print (f'md5 matches the stored value {md5}')
