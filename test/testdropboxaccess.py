import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from configmanager import *
from dropboxaccess import DropboxAccess
			
class TestDropboxAccess(unittest.TestCase):
	def testGetCloudFileList(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
		
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		drpa = DropboxAccess(cm, projectName)

		self.assertEqual(sorted(['my_file_one.py', 'my_file_two.py']), sorted(drpa.getCloudFileList()))

	def testGetCloudFileList_invalid_cloud_dir(self):
		'''
		Tests that the getCloudFileList() method raises a NotADirectoryError
		if the cloud project path which is equal to cloud transfer base dir + 
		'/' + projectName as defined in the tranfiles.ini file does not exist.
		'''
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
		
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'not_exist'
		drpa = DropboxAccess(cm, projectName)
		
		# project name which has an invalid (not existing) project path in the
		# transfiles.ini file
		invalidProjectName = 'transFileCloudInvalidProject'
		self.assertRaises(NotADirectoryError, drpa.getCloudFileList)

if __name__ == '__main__':
	unittest.main()
