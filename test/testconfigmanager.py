import unittest
import os, sys, inspect, datetime
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT
from configmanager import *
			
class TestConfigManager(unittest.TestCase):
	def testConstructor(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)
		
		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Download', cm.downloadPath)
		else:
			self.assertEqual('D:\\\\Users\\\\Jean-Pierre\\\\Downloads', cm.downloadPath)


		self.assertIsNotNone(cm.dropboxApiKey)
		self.assertEqual('/test_dropbox', cm.dropboxBaseDir)

	def testGetProjectLocalDir(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		if os.name == 'posix':
			self.assertEqual('/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud', cm.getProjectLocalDir(projectName))
		else:
			self.assertEqual('D:\\\\Development\\\\Python\\\\trans_file_cloud', cm.getProjectLocalDir(projectName))

	def testGetLastSynchTime(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		self.assertEqual('2020-06-13 08:45:23', cm.getLastSynchTime(projectName))

	def testUpdateLastSynchTime(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		lastSynchTime = cm.getLastSynchTime(projectName)
		cm.updateLastSynchTime(projectName, '2020-06-23 08:45:23')
		self.assertEqual('2020-06-23 08:45:23', cm.getLastSynchTime(projectName))
		
		# restoring old synch time
		cm.updateLastSynchTime(projectName, lastSynchTime)
	@unittest.skip	
	def testGetExcludedDirLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		if os.name == 'posix':
			self.assertEqual(['/test/testproject_2/projectdir', '/test/testproject_3/projectdir'], cm.getExcludedDirLst(projectName))
			
if __name__ == '__main__':
	unittest.main()
	#tst = TestTransferFiles()
	#tst.testUploadModifiedFilesToCloud()
