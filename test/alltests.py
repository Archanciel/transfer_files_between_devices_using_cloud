from unittest import TestLoader, TextTestRunner, TestSuite

from testfilelister import TestFileLister
from testfilemover import TestFileMover

 
if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestFileLister),
                       loader.loadTestsFromTestCase(TestFileMover)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
