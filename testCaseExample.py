import unittest
import os
import tempfile
import shutil
from synchronization import synchronize

class TestSynchronizeFunction(unittest.TestCase):

    def setUp(self):
        # create folders and files
        self.source_folder = tempfile.mkdtemp()
        self.replica_folder = tempfile.mkdtemp()

        self.source_file1 = os.path.join(self.source_folder, 'file1.txt')
        self.source_file2 = os.path.join(self.source_folder, 'file2.txt')
        self.replica_file1 = os.path.join(self.replica_folder, 'file1.txt')

        with open(self.source_file1, 'w') as f:
            f.write('Content of file1')

        with open(self.source_file2, 'w') as f:
            f.write('Content of file2')

        with open(self.replica_file1, 'w') as f:
            f.write('Content of file1_replica')

    def tearDown(self):
        shutil.rmtree(self.source_folder)
        shutil.rmtree(self.replica_folder)


    def test_synchronize(self):
        deleted_files, added_files, changed_files = synchronize(self.source_folder, self.replica_folder)

        # check the results
        self.assertEqual(set(deleted_files), set())
        self.assertEqual(set(added_files), {os.path.basename(self.source_file2)})
        self.assertEqual(set(changed_files), {os.path.basename(self.source_file1)})

        # Check of file content
        with open(os.path.join(self.replica_folder, os.path.basename(self.source_file1)), 'r') as f:
            content = f.read()
            self.assertEqual(content, 'Content of file1')

        # Check of copiyed file
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, os.path.basename(self.source_file2))))

if __name__ == '__main__':
    unittest.main()
