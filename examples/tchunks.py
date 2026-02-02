import os
import time
import shutil
import sys

def delete_dir(directory_to_delete):
    try:
        shutil.rmtree(directory_to_delete)
        print(f"Directory tree '{directory_to_delete}' successfully removed.")
    except OSError as e:
        print(f"Error: {directory_to_delete} : {e.strerror}")

NOW = time.strftime("%y%m%d%H%M%S")

def make_some_files(load_name, sizes, number_of_files =5):
    for size in sizes:
        subname= f"TestFiles_{str(size).zfill(2)}bytes"
        folder_path = os.path.join(load_name, "assets", subname)
        os.makedirs(folder_path, exist_ok=True)
        for i in range(number_of_files):
            test_file_name = f'{subname}_{i}.txt'
            with open(f'{folder_path}/{test_file_name}', 'wb') as f:
                f.write(b'\0' * size)  # Write null bytes

def crawl_dir(inpath):
    '''
    inpath is a string representing a DIRECTORY on the file system
    returns a sorted list of files from inpath
    '''
    filepath_list=[]
    for (path,dirs,files) in os.walk(inpath):
        for item in files:
            filepath = os.path.join(path,item)
            if filepath not in filepath_list:
                filepath_list.append(filepath)
    return sorted(filepath_list)

def make_chunks(inpath, chunks_gb):
    file_paths = crawl_dir(inpath)

    current_chunk_size = 0
    chunk_index = 1
    total_size = 0
    chunks_bytes = int(chunks_gb) * 1000**3
    current_chunk_file_count = 0


    for fp in file_paths:

        # Get the file size
        fp_size = os.path.getsize(fp)

        # Start a new chunk if the current one would exceed chunks_bytes
        if current_chunk_size + fp_size > chunks_bytes:
            chunk_index += 1
            current_chunk_size = 0
            current_chunk_file_count = 0

        current_chunk_size += fp_size
        total_size += fp_size
        current_chunk_file_count += 1

        chunk_dir = f"{inpath}_chunk_{str(chunk_index).zfill(4)}"
        relative_path_to_file = os.path.relpath(fp, start=inpath)
        new_file_path = os.path.join(chunk_dir,relative_path_to_file)
        new_file_dir = os.path.dirname(new_file_path)

        os.makedirs(new_file_dir, exist_ok=True)
        os.rename(fp, new_file_path)

        if os.path.exists(new_file_path):
            print (f"{new_file_path} - {current_chunk_size} of {chunks_bytes} - {current_chunk_file_count} files total")

def example():
    print("Here is an example")
    make_some_files(f"trashme-{NOW}",[5,10,15],10)
    make_some_files(f"trashme-{NOW}",[55],2)
    # null = input("PAUSED")
    make_chunks(f"trashme-{NOW}/assets", 50/(1000**3))
    delete_dir(f"trashme-{NOW}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python tchunks.py <input directory> <chunk size in gigabytes>")
        example()
    else:
        make_chunks(sys.argv[1],sys.argv[2])