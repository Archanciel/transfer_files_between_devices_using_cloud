import unittest
import os, sys, inspect, datetime
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT_CONFIG_FILE
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
			self.assertEqual('D:\\Users\\Jean-Pierre\\Downloads', cm.downloadPath)

	def testConstructorConfigFileNotExist(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles_notExist.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles_notExist.ini'
		
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
			self.assertEqual('D:\\Development\\Python\\trans_file_cloud', cm.getProjectLocalDir(projectName))

	def testGetLastSynchTime(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		self.assertEqual('2020-06-13 08:45:23', cm.getLastSynchTime(projectName))

	def testIsProjectSubDirSynchronized_True(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'exploreProject'
		
		self.assertTrue(cm.isProjectSubDirSynchronized(projectName))

	def testIsProjectSubDirSynchronized_False(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		self.assertFalse(cm.isProjectSubDirSynchronized(projectName))

	def testIsProjectSubDirSynchronized_False_keyNotDefined(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'TransferFilesTestProject'
		
		self.assertFalse(cm.isProjectSubDirSynchronized(projectName))

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
	
	def testGetExcludedDirLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		if os.name == 'posix':
			self.assertEqual(['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir'], cm.getExcludedDirLst(projectName))
		else:
			self.assertEqual(['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir'], cm.getExcludedDirLst(projectName))
	
	def testGetExcludedFileTypeLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		self.assertEqual(['*.pyc', '*.ini', '*.tmp'], cm.getExcludedFileTypeWildchardLst(projectName))
			
	def testGetExcludedFileTypeWildchardLst_noExcludeSection(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles_noExclude.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles_noExclude.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudProject'
		
		self.assertEqual([], cm.getExcludedDirLst(projectName))
			
	def testGetFilePatternLocalDestinationDic(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
		cm = ConfigManager(configFilePathName)		
		projectName = 'transFileCloudTestProject'
		
		if os.name == 'posix':
			self.assertEqual({'*.docx': '/doc',
							 '*.jpg': '/images',
							 '*.md': '',
							 '*.mp3': '/mp3',
							 '*.py': '',
							 '*Solemne*.mp3': '/mp3/solemne',
							 'aa*.jpg': '/images/aa',
							 'test*.py': '/test'}, cm.getFilePatternLocalDestinationDic(projectName))
		else:
			self.assertEqual({'*.docx': '\\doc',
							 '*.jpg': '\\images',
							 '*.md': '',
							 '*.mp3': '\\mp3',
							 '*.py': '',
							 '*Solemne*.mp3': '\\mp3\\solemne',
							 'aa*.jpg': '\\images\\aa',
							 'test*.py': '\\test'}, cm.getFilePatternLocalDestinationDic(projectName))

if __name__ == '__main__':
	unittest.main()
	#tst = TestConfigManager()
	#tst.testGetExcludedDirLst()
