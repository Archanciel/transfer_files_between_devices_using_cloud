import unittest
import os, sys, inspect
from distutils import dir_util
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT
from configmanager import *
from transferfiles import TransferFiles
from dropboxaccess import DropboxAccess
			
class TestTransferFiles(unittest.TestCase):
	def testValidateLastSynchTimeStr_invalid(self):
		tf = TransferFiles(projectName='transFileCloudTestProject')
		lastSynchTimeStr = '2020-13-02 08:09:55'
		self.assertFalse(tf.validateLastSynchTimeStr(lastSynchTimeStr))

	def testValidateLastSynchTimeStrNoZeroInDateTimeString(self):
		tf = TransferFiles(projectName='transFileCloudTestProject')
		lastSynchTimeStr = '2020-6-4 8:5:3'
		self.assertTrue(tf.validateLastSynchTimeStr(lastSynchTimeStr))

	def testValidateLastSynchTimeStrTwoOigitYear(self):
		tf = TransferFiles(projectName='transFileCloudTestProject')
		lastSynchTimeStr = '20-6-4 8:5:3'
		self.assertFalse(tf.validateLastSynchTimeStr(lastSynchTimeStr))

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
		
		cloudFileLst = drpa.getCloudFileList()
		
		for file in cloudFileLst:
			drpa.deleteFile(file)
			
		self.assertEqual([], drpa.getCloudFileList())

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
		
		# selecting project 1 (the test project)
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
		
		self.assertEqual(sorted(expectedUploadedFileNameLst), sorted(drpa.getCloudFileList()))

		# now restoring the modified files dir to its saved version
		dir_util.copy_tree(localProjectDirSaved, localProjectDir)

if __name__ == '__main__':
	unittest.main()
	# tst = TestTransferFiles()
	# tst.testUploadModifiedFilesToCloud()
