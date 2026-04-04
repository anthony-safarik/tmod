# TODO wrap it up, figure out logic and if archiver should be a class or whatever, consider storing the last known bucket name and loading that mani first, figure out storing the config 
import unittest
import os
import shutil
from pathlib import Path
from examples import rename_existing


class TestArchiver(unittest.TestCase):
    """Basic test cases."""

    def create_files(base: Path, files):
        """Helper to create files in a directory structure."""
        for f in files:
            full = base / f
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text("test")

    def setUp(self):

        self.test_root = "trash_testing"

        def make_some_files(load_name, sizes, number_of_files =5):
            for size in sizes:
                subname= f"TestFiles_{str(size).zfill(2)}bytes"
                folder_path = os.path.join(load_name, "assets", subname)
                os.makedirs(folder_path, exist_ok=True)
                for i in range(number_of_files):
                    test_file_name = f'{subname}_{i}.txt'
                    with open(f'{folder_path}/{test_file_name}', 'wb') as f:
                        f.write(b'\0' * size)  # Write null bytes

        make_some_files(f"{self.test_root}/test-ref",[5,10],2)
        make_some_files(f"{self.test_root}/test-src",[5,10,15],1)
        return super().setUp()
    
    def tearDown(self):
        shutil.rmtree(self.test_root)
        return super().tearDown()
    
    def test_main(self):
        non_existing_files = [
        'trash_testing/test-dst/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-dst/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt']

        print("-------")

        for i in non_existing_files:
            print(i,os.path.exists(i))
            assert os.path.exists(i) == False

        existing_files = [
        'trash_testing/test-src/assets/TestFiles_15bytes/TestFiles_15bytes_0.txt',
        'trash_testing/test-src/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-src/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_05bytes/TestFiles_05bytes_1.txt',
        'trash_testing/test-ref/assets/TestFiles_10bytes/TestFiles_10bytes_1.txt']

        print("-------")
        for i in existing_files:
            print(i,os.path.exists(i))
            assert os.path.exists(i) == True

        src = Path(self.test_root) / 'test-src'
        ref = Path(self.test_root) / 'test-ref'
        dst = Path(self.test_root) / 'test-dst'

        print("-------")
        rename_existing.main(src, ref, dst)

        existing_files = [
        'trash_testing/test-src/assets/TestFiles_15bytes/TestFiles_15bytes_0.txt',
        'trash_testing/test-dst/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-dst/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt',
        'trash_testing/test-ref/assets/TestFiles_05bytes/TestFiles_05bytes_1.txt',
        'trash_testing/test-ref/assets/TestFiles_10bytes/TestFiles_10bytes_1.txt']

        print("-------")

        for i in existing_files:
            print(i,os.path.exists(i))
            assert os.path.exists(i) == True

        non_existing_files = [
        'trash_testing/test-src/assets/TestFiles_05bytes/TestFiles_05bytes_0.txt',
        'trash_testing/test-src/assets/TestFiles_10bytes/TestFiles_10bytes_0.txt']

        print("-------")

        for i in non_existing_files:
            print(i,os.path.exists(i))
            assert os.path.exists(i) == False

if __name__ == '__main__':
    unittest.main()