import os
import shutil

def compare_and_move_matching_files(src_folder, cmp_folder, move_folder):
    """
    Recursively compares one directory to another and moves out any matching files.
    Skips hidden files and folders.
    
    :param src_folder: Source folder to check for files
    :param cmp_folder: Comparison folder to find matching files
    :param move_folder: Folder to move matching files into
    """
    if not os.path.exists(move_folder):
        os.makedirs(move_folder)

    for root, dirs, files in os.walk(src_folder):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        relative_folder_path = os.path.relpath(root, src_folder)
        move_target_dir = os.path.join(move_folder, relative_folder_path)

        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, src_folder)
            cmp_file_path = os.path.join(cmp_folder, relative_file_path)
            move_file_path = os.path.join(move_folder, relative_file_path)

            # Skip hidden files
            if file.startswith("."):
                continue

            # Check if the file exists in the comparison directory
            if os.path.exists(cmp_file_path):
                print(f"Exist:True....{cmp_file_path}")

                # Ensure the target directory exists
                if not os.path.exists(move_target_dir):
                    os.makedirs(move_target_dir)

                # Move the file to the relative target directory
                shutil.move(file_path, move_file_path)
            else:
                print(f"Exist:False...{cmp_file_path}")



if __name__ == "__main__":

    # temp folders for testing
    src_folder = "temp/src"
    cmp_folder = "temp/dst"
    move_folder = "temp/src_moved"

    # Make subfolders and files for testing
    subfolder1 = "temp/src/banana"
    subfolder2 = "temp/src/grape"
    subfolder3 = "temp/dst/banana"
    subfolder4 = "temp/dst/strawberry"
    subfolders = (subfolder1,subfolder2,subfolder3,subfolder4)
    for subfolder in subfolders:
        os.makedirs(subfolder, exist_ok=True)
        fname = os.path.join(subfolder,"tempfile.txt")
        with open(fname, 'w') as file:
            # Write some sample text
            file.write("temp file for testing only")

    compare_and_move_matching_files(src_folder, cmp_folder, move_folder)