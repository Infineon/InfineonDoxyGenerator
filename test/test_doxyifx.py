import unittest, os, shutil, subprocess, sys
sys.path.append('./..')
import doxyifx as doxi

class TestDoxygenIFX(unittest.TestCase):

    build_dir = './../build/test_temp'
    repo_url = 'https://github.com/owner/repository-name.git'
    
    @classmethod
    def setUpClass(self):
        # Create temporary repo mock folder
        if not os.path.exists(TestDoxygenIFX.build_dir):
            os.makedirs(TestDoxygenIFX.build_dir)
        # Move to repo folder
        os.chdir(TestDoxygenIFX.build_dir)
        # Init repo
        FNULL = open(os.devnull, 'w')
        p1 = subprocess.Popen(['git', 'init'], stdout=FNULL)
        p1.wait()
        # Set url
        p2 = subprocess.Popen(['git', 'remote', 'add', 'origin', TestDoxygenIFX.repo_url])
        p2.wait()

    @classmethod
    def tearDownClass(self):
        os.chdir('./..')
        # Remove temporary repository folder
        shutil.rmtree(TestDoxygenIFX.build_dir)
    

    def test_get_repo_url_OK(self):
        """
        Gets repo url OK
        """
        repo_url = doxi.get_repo_url()
        self.assertEqual(repo_url,TestDoxygenIFX.repo_url)

    
    def test_get_repo_owner_OK(self):
        """
        Gets repo owner OK
        """
        repo_owner = doxi.get_repo_owner(TestDoxygenIFX.repo_url)
        self.assertEqual(repo_owner,'owner')

    def test_get_repo_name_OK(self):
        """
        Gets repo name OK
        """
        repo_name = doxi.get_repo_name(TestDoxygenIFX.repo_url)
        self.assertEqual(repo_name,'repository-name')
    


if __name__ == '__main__':
    unittest.main(verbosity=2)