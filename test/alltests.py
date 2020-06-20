from unittest import TestLoader, TextTestRunner, TestSuite

from testfilelister import TestFileLister
from testfilemover import TestFileMover
from testrequester import TestRequester
from testdropboxaccess import TestDropboxAccess
 
if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestFileLister),
                       loader.loadTestsFromTestCase(TestFileMover),
                       loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestDropboxAccess)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
