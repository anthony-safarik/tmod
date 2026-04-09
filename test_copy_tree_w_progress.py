import unittest
import os
import shutil
from pathlib import Path
from examples import copy_tree_w_progress_v1 as copy_tree


class TestCopyTree(unittest.TestCase):
    """Basic test cases."""

    def create_files(base: Path, files):
        """Helper to create files in a directory structure."""
        for f in files:
            full = base / f
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text("test")

    def setUp(self):

        self.test_root = "trash_testing"
        self.src = f"{self.test_root}/test-src"
        self.dst = f"{self.test_root}/test-dst"

        def make_some_files(load_name, sizes, number_of_files =5):
            for size in sizes:
                subname= f"TestFiles_{str(size).zfill(2)}bytes"
                folder_path = os.path.join(load_name, "assets", subname)
                os.makedirs(folder_path, exist_ok=True)
                for i in range(number_of_files):
                    test_file_name = f'{subname}_{i}.txt'
                    with open(f'{folder_path}/{test_file_name}', 'wb') as f:
                        f.write(b'\0' * size)  # Write null bytes

        make_some_files(self.src,[5,10,15,20],1)

        return super().setUp()
    
    def tearDown(self):
        shutil.rmtree(self.test_root)
        return super().tearDown()
    
    def test_main(self):
        copy_tree.copy_tree_w_progress(self.src,self.dst,True)
        copy_tree.copy_tree_w_progress(self.src,self.dst,False)

if __name__ == '__main__':
    unittest.main()