import unittest
import os, sys, inspect, datetime
from distutils import dir_util
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT_CONFIG_FILE
from configmanager import *
from transferfiles import TransferFiles
from dropboxaccess import DropboxAccess
from filelister import FileLister
			
class TestTransferFiles(unittest.TestCase):
	def testValidateLastSynchTimeStr_invalid(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		projectName = 'TransferFilesTestProject'
		tf = TransferFiles(configFilePath=configFilePathName, projectName=projectName)
		lastSynchTimeStr = '2020-13-02 08:09:55'
		isValid, validLastSynchTimeStr = tf.validateLastSynchTimeStr(lastSynchTimeStr)
		self.assertFalse(isValid)
		self.assertEqual('', validLastSynchTimeStr)

	def testValidateLastSynchTimeStrNoZeroInDateTimeString(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		projectName = 'TransferFilesTestProject'
		tf = TransferFiles(configFilePath=configFilePathName, projectName=projectName)
		lastSynchTimeStr = '2020-6-4 8:5:3'
		self.assertTrue(tf.validateLastSynchTimeStr(lastSynchTimeStr))

	def testValidateLastSynchTimeStrTwoDigitYear(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		projectName = 'TransferFilesTestProject'
		tf = TransferFiles(configFilePath=configFilePathName, projectName=projectName)
		lastSynchTimeStr = '20-6-4 8:5:3'
		isValid, validLastSynchTimeStr = tf.validateLastSynchTimeStr(lastSynchTimeStr)
		self.assertTrue(isValid)
		self.assertEqual('2020-06-04 08:05:03', validLastSynchTimeStr)

	def testValidateLastSynchTimeStrDateOnly(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		projectName = 'TransferFilesTestProject'
		tf = TransferFiles(configFilePath=configFilePathName, projectName=projectName)
		lastSynchTimeStr = '20-6-4'
		isValid, validLastSynchTimeStr = tf.validateLastSynchTimeStr(lastSynchTimeStr)
		self.assertTrue(isValid)
		self.assertEqual('2020-06-04 00:00:00', validLastSynchTimeStr)

	def testUploadModifiedFilesToCloud(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

		if os.name == 'posix':
			localProjectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir'
			localProjectDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir_saved'
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			localProjectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir'
			localProjectDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir_saved'
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'
		
		# cleaning up the target cloud folder
		
		cm = ConfigManager(configFilePathName)
		projectName = 'TransferFilesTestProject'
		drpa = DropboxAccess(cm, projectName)
		
		cloudFileLst = drpa.getCloudFileNameList()
		
		for file in cloudFileLst:
			drpa.deleteFile(file)
			
		self.assertEqual([], drpa.getCloudFileNameList())

		# reading and rewriting test project files to update their modification date

		tstFileToModifyLst = ['testfilemover_2.py']
		pythonFileToModifyLst = ['filemover_2.py', 'filelister_2.py']
		docFileToModifyLst = ['doc_21.docx', 'doc_22.docx']
		imgFileToModifyLst = ['current_state_21.jpg']

		tstFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'test' + DIR_SEP + x for x in tstFileToModifyLst]
		pythonFilePathNameToModifyLst = [localProjectDir + DIR_SEP + x for x in pythonFileToModifyLst]
		docFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'doc' + DIR_SEP + x for x in docFileToModifyLst]
		imgFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'images' + DIR_SEP + x for x in imgFileToModifyLst]

		filePathNameToModifyLst = tstFilePathNameToModifyLst + pythonFilePathNameToModifyLst + docFilePathNameToModifyLst + imgFilePathNameToModifyLst

		for filePathName in filePathNameToModifyLst:
			# opening file as readwrite in binary mode
			with open(filePathName, 'rb+') as f:
				content = f.read()
				f.seek(0)
				f.write(content)
				f.close()

		# simulating user input

		stdin = sys.stdin
		
		# selecting project 1 (the test project 'TransferFilesTestProject' is
		# the first project defined in test_TransferFiles.ini !)
		sys.stdin = StringIO('1')

		print('\nstdout temporarily captured. Test is running ...')
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		# now asking TransferFiles to upload the modified files 
		
		tf = TransferFiles(configFilePath=configFilePathName)
		
		# confirming modified files upload
		sys.stdin = StringIO('Y')
		
		tf.uploadModifiedFilesToCloud()

		sys.stdin = stdin
		sys.stdout = stdout
		
		expectedUploadedFileNameLst = tstFileToModifyLst + pythonFileToModifyLst + docFileToModifyLst + imgFileToModifyLst
		
		self.assertEqual(sorted(expectedUploadedFileNameLst), sorted(drpa.getCloudFileNameList()))

		# now restoring the modified files dir to its saved version
		dir_util.copy_tree(localProjectDirSaved, localProjectDir)

	def testPathUploadToCloud(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

		if os.name == 'posix':
			localProjectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir'
			localProjectDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir_saved'
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			localProjectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir'
			localProjectDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir_saved'
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		# cleaning up the target cloud folder

		cm = ConfigManager(configFilePathName)
		projectName = 'TransferFilesTestProject'
		drpa = DropboxAccess(cm, projectName)

		cloudFileLst = drpa.getCloudFilePathNameList()

		for file in cloudFileLst:
			drpa.deleteFile(file)
		
		self.assertEqual([], drpa.getCloudFilePathNameList())

		# reading and rewriting test project files to update their modification date

		tstFileToUploadLst = ['testfilemover_2.py']
		pythonFileToUploadLst = ['filemover_2.py', 'filelister_2.py']
		docFileToUploadLst = ['doc_21.docx', 'doc_22.docx']
		imgFileToUploadLst = ['current_state_21.jpg']

		tstFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'test' + DIR_SEP + x for x in tstFileToUploadLst]
		pythonFilePathNameToUploadLst = [localProjectDir + DIR_SEP + x for x in pythonFileToUploadLst]
		docFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'doc' + DIR_SEP + x for x in docFileToUploadLst]
		imgFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'images' + DIR_SEP + x for x in imgFileToUploadLst]

		filePathNameToUploadLst = tstFilePathNameToUploadLst + pythonFilePathNameToUploadLst + docFilePathNameToUploadLst + imgFilePathNameToUploadLst

		# simulating user input

		stdin = sys.stdin

		# selecting project 1 (the test project 'TransferFilesTestProject' is
		# the first project defined in test_TransferFiles.ini !)
		sys.stdin = StringIO('1')

		print('\nstdout temporarily captured. Test is running ...')

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		# now asking TransferFiles to upload the modified files

		tf = TransferFiles(configFilePath=configFilePathName)
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		tf.pathUploadToCloud(filePathNameToUploadLst)

		sys.stdin = stdin
		sys.stdout = stdout

		expectedUploadedFilePathNameLst = ['doc/doc_21.docx',
										   'doc/doc_22.docx',
										   'filelister_2.py',
										   'filemover_2.py',
										   'images/current_state_21.jpg',
										   'test/testfilemover_2.py']

		actualUploadedFilePathNameLst = drpa.getCloudFilePathNameList()
		self.assertEqual(sorted(expectedUploadedFilePathNameLst), sorted(actualUploadedFilePathNameLst))
		#print(outputCapturingString.getvalue())
		if os.name == 'posix':
			self.assertTrue('Uploading testproject_2/projectdir/test/testfilemover_2.py to the cloud .../n' +
							 'Uploading test/testproject_2/projectdir/filemover_2.py to the cloud .../n' +
							 'Uploading test/testproject_2/projectdir/filelister_2.py to the cloud .../n' +
							 'Uploading testproject_2/projectdir/doc/doc_21.docx to the cloud .../n' +
							 'Uploading testproject_2/projectdir/doc/doc_22.docx to the cloud .../n' +
							 'Uploading testproject_2/projectdir/images/current_state_21.jpg to the cloud ...)\n' in outputCapturingString.getvalue())
		else:
			self.assertTrue('Uploading testproject_2\projectdir\\test\\testfilemover_2.py to the cloud ...\n' +
							'Uploading test\\testproject_2\projectdir\\filemover_2.py to the cloud ...\n' +
							'Uploading test\\testproject_2\projectdir\\filelister_2.py to the cloud ...\n' +
							'Uploading testproject_2\projectdir\doc\doc_21.docx to the cloud ...\n' +
							'Uploading testproject_2\projectdir\doc\doc_22.docx to the cloud ...\n' +
							'Uploading testproject_2\projectdir\images\current_state_21.jpg to the cloud ...)\n' in outputCapturingString.getvalue())

	def testTransferFilesFromCloudToLocalDirs(self):
		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

		if os.name == 'posix':
			localProjectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir'
			localProjectDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir_saved'
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			localProjectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir'
			localProjectDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir_saved'
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'
				
		cm = ConfigManager(configFilePathName)
		projectName = 'TransferFilesTestProject'
		
		# storing the last synch update time to compare it to the new update 
		# time once download and move has been performed
		storedLastSynchTimeStr = cm.getLastSynchTime(projectName)
		storedLastSyncTime = datetime.datetime.strptime(storedLastSynchTimeStr, DATE_TIME_FORMAT_CONFIG_FILE)
		
		# cleaning up the cloud folder before uploading the test files
				
		drpa = DropboxAccess(cm, projectName)
		
		cloudFileLst = drpa.getCloudFileNameList()
		
		for file in cloudFileLst:
			drpa.deleteFile(file)
			
		self.assertEqual([], drpa.getCloudFileNameList())

		# listing the test files which wiLl be uploaded to
		# the cloud in order to be available for download
		# and move to local dirs

		tstFileToUploadLst = ['testfilemover_2.py']
		pythonFileToUploadLst = ['filemover_2.py', 'filelister_2.py']
		docFileToUploadLst = ['doc_21.docx', 'doc_22.docx']
		imgFileToUploadLst = ['current_state_21.jpg']
		
		fileNameToUploadLst = tstFileToUploadLst + pythonFileToUploadLst + docFileToUploadLst + imgFileToUploadLst

		tstFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'test' + DIR_SEP + x for x in tstFileToUploadLst]
		pythonFilePathNameToUploadLst = [localProjectDir + DIR_SEP + x for x in pythonFileToUploadLst]
		docFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'doc' + DIR_SEP + x for x in docFileToUploadLst]
		imgFilePathNameToUploadLst = [localProjectDir + DIR_SEP + 'images' + DIR_SEP + x for x in imgFileToUploadLst]

		filePathNameToUploadLst = tstFilePathNameToUploadLst + pythonFilePathNameToUploadLst + docFilePathNameToUploadLst + imgFilePathNameToUploadLst

		# uploading the test files which will then be downloaded and moved to
		# local dirs
		
		drpa = DropboxAccess(cm, projectName)
		
		for filePathName in filePathNameToUploadLst:
			drpa.uploadFileName(filePathName)

		# simulating user input

		stdin = sys.stdin
		
		# selecting project 1 (the test project 'TransferFilesTestProject' is
		# the first project defined in test_TransferFiles.ini !)
		sys.stdin = StringIO('1')

		print('\nstdout temporarily captured. Test is running ...')
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		# now asking TransferFiles to download the cloud files and move them
		# to the local dirs
		
		tf = TransferFiles(configFilePath=configFilePathName)
		
		# confirming cloud files download
		sys.stdin = StringIO('Y')
		
		tf.transferFilesFromCloudToLocalDirs(drpa.getCloudFileNameList())

		sys.stdin = stdin
		sys.stdout = stdout
		
		# testing that the last synch time is after the stored synch time
		
		cm_reloaded = ConfigManager(configFilePathName)
		newLastSynchTimeStr = cm_reloaded.getLastSynchTime(projectName)
		newLastSyncTime = datetime.datetime.strptime(newLastSynchTimeStr, DATE_TIME_FORMAT_CONFIG_FILE)
		self.assertTrue(newLastSyncTime > storedLastSyncTime)
		
		# now testing that the files downloaded from the cloud and moved to
		# the local dirs are the expected ones
		
		# first, reset the last synch time to the stored one so that FileLister
		# will list files whose modification date is oreater than this time
		cm.updateLastSynchTime(projectName, storedLastSynchTimeStr)
		
		fl = FileLister(cm)
		allFileNameLst, allFilePathNameLst, lastSyncTimeStr = fl.getModifiedFileLst(projectName)
		
		self.assertEqual(sorted(fileNameToUploadLst), sorted(allFileNameLst))
		self.assertEqual(sorted(filePathNameToUploadLst), sorted(allFilePathNameLst))

		# now restoring the modified files dir to its saved version
		dir_util.copy_tree(localProjectDirSaved, localProjectDir)

	def testTransferFilesConstructor_commandLine_invalProject(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_TransferFiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_TransferFiles.ini'

		old_sys_argv = sys.argv
		sys.argv = [old_sys_argv[0]] + ['-pinvalProjName']

		tf = TransferFiles(configFilePathName)
		
		# if not done, perturbates the next unit tests !
		sys.argv = old_sys_argv

		self.assertEqual(None, tf.projectName)

if __name__ == '__main__':
	#unittest.main()
	tst = TestTransferFiles()
	tst.testPathUploadToCloud()
