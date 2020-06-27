import unittest
import os, sys, inspect, datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT
from configmanager import *
from dropboxaccess import DropboxAccess
			
class TestDropboxAccess(unittest.TestCase):
	def testGetCloudFileList(self):
		"""
		For this test to succeed, the dropbox test dir must contain two files:
		my_file_one.py and my_file_two.py. 
		
		The dropbox cloud folder is test_dropbox/transFileCloudTestProject
		"""	
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

	def testCreateEmptyFolder(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
		
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		newFolderName = 'newFolder'
		
		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName + '/' + newFolderName)
		self.assertRaises(NotADirectoryError, drpa.getCloudFileList)
		
		# now, creating the new folder. First recreate a DropboxAccess
		# on an existing project folder
		drpa = DropboxAccess(cm, projectName)
		
		# then create the new folder and ensure it is accessible
		drpa.createEmptyFolder(newFolderName)
		
		# creating a DropboxAccess on the newly created Dropbox folder
		# to ensure the folder now exists
		drpa = DropboxAccess(cm, projectName + '/' + newFolderName)
		
		# should not raise any error
		drpa.getCloudFileList()
		
		# now deleting the newly created folder so that other tests are not
		# impacted
		drpa = DropboxAccess(cm, projectName)
		drpa.deleteFolder(newFolderName)

	def testCreateAndDeleteProjectFolder(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectToCreate'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		self.assertRaises(NotADirectoryError, drpa.getCloudFileList)

		# now, creating the project folder
		drpa.createProjectFolder()

		# should not raise any error
		drpa.getCloudFileList()

		# now deleting the newly created folder so that this test can be run again
		drpa = DropboxAccess(cm, projectName)
		drpa.deleteProjectFolder()

		# verify the project folder was deleted
		self.assertRaises(NotADirectoryError, drpa.getCloudFileList)
		
	def testUploadAndDeleteFile(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			localDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			localDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectForUpload'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		
		try:
			drpa.getCloudFileList()
		except NotADirectoryError:
			# if project folder does not exist
			drpa.createProjectFolder()

		# should not raise any error
		self.assertEqual([], drpa.getCloudFileList())
		
		# now, uploading a file
		uploadFileName = 'filemover_1.py'
		localFilePathName = localDir + DIR_SEP + uploadFileName
		drpa.uploadFile(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileList())
		
		# now deleting the newly created file so that this test can be run again
		drpa.deleteFile(uploadFileName)
		
		# should not raise any error
		self.assertEqual([], drpa.getCloudFileList())		
		
	def testUploadSameFileTwice(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			localDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			localDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectForUpload'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		
		try:
			drpa.getCloudFileList()
		except NotADirectoryError:
			# if project folder does not exist
			drpa.createProjectFolder()

		# should not raise any error
		self.assertEqual([], drpa.getCloudFileList())
		
		# now, uploading a file
		uploadFileName = 'uploadTwice'
		localFilePathName = localDir + DIR_SEP + uploadFileName
		drpa.uploadFile(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileList())

		# modifiying the file before uploading it again. Since 
		# dropbox.files.WriteMode.overwrite is set when calling
		# dropbox.files_upload, no WriteConflictError is raised
		# when uploading the modified file.
		with open(localFilePathName, 'w') as f:
			f.write('modified at date {}'.format(datetime.datetime.now().strftime(DATE_TIME_FORMAT)))
			f.close()

		drpa.uploadFile(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileList())
		# now deleting the newly created file so that this test can be run again
		drpa.deleteFile(uploadFileName)
		
		# should not raise any error
		self.assertEqual([], drpa.getCloudFileList())		

if __name__ == '__main__':
	unittest.main()
#	tst = TestDropboxAccess()
#	tst.testUploadSameFileTwice()
