import unittest
import os, sys, inspect, datetime, glob, shutil

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT_CONFIG_FILE
from configmanager import *
from dropboxaccess import DropboxAccess
			
class TestDropboxAccess(unittest.TestCase):
	def testGetCloudFileNameList(self):
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

		self.assertEqual(sorted(['my_file_one.py', 'my_file_two.py']), sorted(drpa.getCloudFileNameList()))

	def testGetCloudFilePathNameList(self):
		"""
		For this test to succeed, the dropbox test dir must contain four files:
		my_file_one.py, my_file_two.py, SubDirOne/subDirOne.py and
		SubDirTwo/subDirTwo.py

		The dropbox cloud folder is test_dropbox/transFileCloudTestProject
		"""
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		drpa = DropboxAccess(cm, projectName)

		self.assertEqual(sorted(['SubDirOne/SubDirOneSubDir/subDirOneSubDir.py',
								 'SubDirOne/subDirOne.py',
								 'SubDirTwo/subDirTwo.py',
								 'my_file_one.py',
								 'my_file_two.py']), sorted(drpa.getCloudFilePathNameList()))

	def testGetCloudFileList_invalid_cloud_dir(self):
		'''
		Tests that the getCloudFileNameList() method raises a NotADirectoryError
		if the cloud project path which is equal to cloud transfer base dir + 
		'/' + projectName as defined in the tranfiles.ini file does not exist.
		'''
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
	
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/dropbox_access_tst.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\dropbox_access_tst.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'not_exist'
		drpa = DropboxAccess(cm, projectName)
		
		# project name which has an invalid (not existing) project path in the
		# transfiles.ini file
		invalidProjectName = 'transFileCloudInvalidProject'
		self.assertRaises(NotADirectoryError, drpa.getCloudFileNameList)

	def testCreateEmptyFolder(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
		
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/dropbox_access_tst.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\dropbox_access_tst.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		newFolderName = 'newFolder'
		
		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName + '/' + newFolderName)
		self.assertRaises(NotADirectoryError, drpa.getCloudFileNameList)
		
		# now, creating the new folder. First recreate a DropboxAccess
		# on an existing project folder
		drpa = DropboxAccess(cm, projectName)
		
		# then create the new folder and ensure it is accessible
		drpa.createProjectSubFolder(newFolderName)
		
		# creating a DropboxAccess on the newly created Dropbox folder
		# to ensure the folder now exists
		drpa = DropboxAccess(cm, projectName + '/' + newFolderName)
		
		# should not raise any error
		drpa.getCloudFileNameList()
		
		# now deleting the newly created folder so that other tests are not
		# impacted
		drpa = DropboxAccess(cm, projectName)
		drpa.deleteProjectSubFolder(newFolderName)

	def testCreateAndDeleteProjectFolder(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/dropbox_access_tst.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\dropbox_access_tst.ini'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectToCreate'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		self.assertRaises(NotADirectoryError, drpa.getCloudFileNameList)

		# now, creating the project folder
		drpa.createProjectFolder()

		# should not raise any error
		drpa.getCloudFileNameList()

		# now deleting the newly created folder so that this test can be run again
		drpa = DropboxAccess(cm, projectName)
		drpa.deleteProjectFolder()

		# verify the project folder was deleted
		self.assertRaises(NotADirectoryError, drpa.getCloudFileNameList)
		
	def testUploadAndDeleteFileName(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/dropbox_access_tst.ini'
			localDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\dropbox_access_tst.ini'
			localDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectForUpload'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		
		try:
			drpa.getCloudFileNameList()
		except NotADirectoryError:
			# if project folder does not exist
			drpa.createProjectFolder()

		# should not raise any error
		self.assertEqual([], drpa.getCloudFileNameList())
		
		# now, uploading a file
		uploadFileName = 'filemover_1.py'
		localFilePathName = localDir + DIR_SEP + uploadFileName
		drpa.uploadFileName(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileNameList())
		
		# now deleting the newly created file so that this test can be run again
		drpa.deleteFile(uploadFileName)
		
		# should not raise any error
		self.assertEqual([], drpa.getCloudFileNameList())		
		
	def testUploadSameFileNameTwice(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/dropbox_access_tst.ini'
			localDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\dropbox_access_tst.ini'
			localDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProjectForUpload'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)
		
		try:
			drpa.getCloudFileNameList()
		except NotADirectoryError:
			# if project folder does not exist
			drpa.createProjectFolder()

		# should not raise any error
		self.assertEqual([], drpa.getCloudFileNameList())
		
		# now, uploading a file
		uploadFileName = 'uploadTwice'
		localFilePathName = localDir + DIR_SEP + uploadFileName
		drpa.uploadFileName(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileNameList())

		# modifiying the file before uploading it again. Since 
		# dropbox.files.WriteMode.overwrite is set when calling
		# dropbox.files_upload, no WriteConflictError is raised
		# when uploading the modified file.
		with open(localFilePathName, 'w') as f:
			f.write('modified at date {}'.format(datetime.datetime.now().strftime(DATE_TIME_FORMAT_CONFIG_FILE)))
			f.close()

		drpa.uploadFileName(localFilePathName)

		self.assertEqual([uploadFileName], drpa.getCloudFileNameList())
		# now deleting the newly created file so that this test can be run again
		drpa.deleteFile(uploadFileName)
		
		# should not raise any error
		self.assertEqual([], drpa.getCloudFileNameList())		

	def testUploadAndDeleteFilePathName(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			localDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			localDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudFilePathNameProject'

		# creating a DropboxAccess on an inexisting Dropbox folder
		# to ensure the folder does not exist
		drpa = DropboxAccess(cm, projectName)

		try:
			drpa.getCloudFileNameList()
		except NotADirectoryError:
			# if project folder does not exist
			drpa.createProjectFolder()

		# should not raise any error
		self.assertEqual([], drpa.getCloudFileNameList())

		# now, uploading two files, one in the root of project dir, the other
		# in a project sub dir
		localProjectDir = cm.getProjectLocalDir(projectName)
		uploadFileNameProjectRoot = 'filemover_2.py'
		localFilePathName = localDir + DIR_SEP + uploadFileNameProjectRoot
		drpa.uploadFilePathName(localFilePathName)

		uploadFileNameProjectSubdir = 'test' + DIR_SEP + 'testfilemover_2.py'
		localFilePathName = localDir + DIR_SEP + uploadFileNameProjectSubdir
		drpa.uploadFilePathName(localFilePathName)

		uploadFileNameProjectSubdirSlashDirSep = uploadFileNameProjectSubdir.replace('\\', '/')
		self.assertEqual([uploadFileNameProjectRoot, uploadFileNameProjectSubdirSlashDirSep], drpa.getCloudFilePathNameList())

		# now deleting the newly created file so that this test can be run again
		drpa.deleteFile(uploadFileNameProjectRoot)
		drpa.deleteFile(uploadFileNameProjectSubdirSlashDirSep)

		# should not raise any error
		self.assertEqual([], drpa.getCloudFilePathNameList())
		drpa.deleteProjectFolder()

	def testDownloadFile(self):
		"""
		For this test to succeed, the dropbox test dir must contain two files:
		my_file_one.py and my_file_two.py.

		The dropbox cloud folder is test_dropbox/transFileCloudTestProject
		"""
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			downloadDir = '/storage/emulated/0/Download'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			downloadDir = 'D:\\Users\\Jean-Pierre\\Downloads'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		drpa = DropboxAccess(cm, projectName)
		fileName = 'my_file_one.py'
		downloadedFilePathName = downloadDir + DIR_SEP + fileName
		drpa.downloadFile(fileName, downloadedFilePathName)

		# verifying that the file was downloaded
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.py')]
		self.assertEqual(sorted([fileName]), sorted(fileNameLst))

		# deleting downloaded file
		os.remove(downloadedFilePathName)

	def testDownloadFile_in_subDir(self):
		"""
		For this test to succeed, the dropbox test dir must contain one file:
		SubDirOne/subDirOne.py.

		The dropbox cloud folder is test_dropbox/transFileCloudTestProject
		"""
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			downloadDir = '/storage/emulated/0/Download'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			downloadDir = 'D:\\Users\\Jean-Pierre\\Downloads'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		drpa = DropboxAccess(cm, projectName)
		fileName = 'subDirOne.py'
		fileSubDir = 'SubDirOne'
		cloudFilePathName = fileSubDir + '/' + fileName
		downloadedFilePathName = downloadDir + DIR_SEP + fileSubDir + DIR_SEP + fileName
		drpa.downloadFile(cloudFilePathName, downloadedFilePathName)

		# verifying that the file was downloaded
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + fileSubDir + DIR_SEP + '*.py')]
		self.assertEqual(sorted([fileName]), sorted(fileNameLst))

		# deleting downloaded file
		shutil.rmtree(downloadDir + DIR_SEP + fileSubDir)

	def testDownloadFile_in_subSubDir(self):
		"""
		For this test to succeed, the dropbox test dir must contain one file:
		SubDirOne/subDirOne.py.

		The dropbox cloud folder is test_dropbox/transFileCloudTestProject
		"""
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			downloadDir = '/storage/emulated/0/Download'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			downloadDir = 'D:\\Users\\Jean-Pierre\\Downloads'

		cm = ConfigManager(configFilePathName)
		projectName = 'transFileCloudTestProject'
		drpa = DropboxAccess(cm, projectName)
		fileName = 'subDirOneSubDir.py'
		fileSubDir = 'SubDirOne'
		fileSubSubDir = 'SubDirOneSubDir'
		cloudFilePathName = fileSubDir + '/' + fileSubSubDir + '/' + fileName
		downloadedFilePathName = downloadDir + DIR_SEP + fileSubDir + DIR_SEP + fileSubSubDir + DIR_SEP + fileName
		drpa.downloadFile(cloudFilePathName, downloadedFilePathName)

		# verifying that the file was downloaded
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + fileSubDir + DIR_SEP + fileSubSubDir + DIR_SEP + '*.py')]
		self.assertEqual(sorted([fileName]), sorted(fileNameLst))

		# deleting downloaded file
		shutil.rmtree(downloadDir + DIR_SEP + fileSubDir)

if __name__ == '__main__':
	unittest.main()
#	tst = TestDropboxAccess()
#	tst.testDownloadFile_in_subSubDir()
