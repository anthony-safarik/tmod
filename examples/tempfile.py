#Make and delete a file
import os

def make_temp_file(temp_file_name, contents = 'Temp File'):
    with open(temp_file_name, 'w') as file:
        # Write some sample text
        file.write(contents)
        print(f'Temp file {temp_file_name} created')


def delete(x):
    """Delete a file x"""
    if os.path.exists(x):
        os.remove(x)
        print(f"File '{x}' deleted successfully.")
    else:
        print(f"File '{x}' does not exist.")

if __name__ == "__main__":
    fname = 'tempfile.txt'
    make_temp_file(fname,'tempfile created by running tempfile.py')
    delete(fname)