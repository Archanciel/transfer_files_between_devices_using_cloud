import unittest
import os, sys, inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager
from requester import Requester

class TestRequester(unittest.TestCase):
	def testGetProjectName(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)
		
		# simulating user input
		stdin = sys.stdin
		sys.stdin = StringIO('2')
 
		self.assertEqual('transFileCloudProject', rq.getProjectName(None))
		
		sys.stdin = stdin
		
	def testGetProjectNameInvalidUserInput(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)
		
		# simulating user input
		stdin = sys.stdin
		sys.stdin = StringIO('0')
 
		self.assertEqual('transFileCloudProject', rq.getProjectName(None))
		
		sys.stdin = stdin
		
	def testGetProjectNameInvalidUserInput_(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)
		
		# simulating user input
		stdin = sys.stdin
		sys.stdin = StringIO('100')
 
		self.assertEqual('transFileCloudProject', rq.getProjectName(None))
		
		sys.stdin = stdin
		
if __name__ == '__main__':
	unittest.main()
