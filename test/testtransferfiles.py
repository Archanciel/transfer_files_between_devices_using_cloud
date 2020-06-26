import unittest
import os, sys, inspect, datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT
from configmanager import *
from transferfiles import TransferFiles
			
class TestTransferFiles(unittest.TestCase):
	def testValidateLastSynchTimeStr_invalid(self):
		tf = TransferFiles()
		lastSynchTimeStr = '2020-13-02 08:09.55'
		self.assertFalse(tf.validateLastSynchTimeStr(lastSynchTimeStr))

if __name__ == '__main__':
	unittest.main()
#	tst = TestDropboxAccess()
#	tst.testUploadSameFileTwice()
