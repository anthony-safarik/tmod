import subprocess
import os

def rcopy(src, dst, flags = ['-a']):
    """Copy file with attributes using rsync"""
    cmd = ['rsync'] + flags + [src, dst]
    subprocess.run(cmd)

def delete(x):
    """Delete a file x"""
    if os.path.exists(x):
        os.remove(x)
        print(f"File '{x}' deleted successfully.")
    else:
        print(f"File '{x}' does not exist.")

if __name__ == "__main__":

    fname_src = 'temp_src.txt'
    fname_dst = 'temp_dst.txt'
    fname_dst_with_flags = 'temp_flags.txt'

    # Make an empty file
    with open(fname_src, 'w') as file:
        # Write some sample text
        file.write('Temp file created by rcopy')
        print(f'Temp file {fname_src} created by rcopy')

    # Make a copy
    rcopy(fname_src, fname_dst)
    flags = ['-a', '--verbose', '--dry-run', '--stats', '--itemize-changes', '--remove-source-files']
    rcopy(fname_src, fname_dst_with_flags, flags)
    
     # Clean up
    for x in[fname_src, fname_dst, fname_dst_with_flags]: delete(x)