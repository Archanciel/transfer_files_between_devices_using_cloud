import unittest
import os, sys, inspect, datetime
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
		
import warnings 		

from constants import DIR_SEP, DATE_TIME_FORMAT
from configmanager import *
from transferfiles import TransferFiles
			
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

#	def testUploadModifiedFilesToCloud(self):
#		# avoid warning resourcewarning unclosed ssl.sslsocket due to Dropbox
#		warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

#		if os.name == 'posix':
#			localProjectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir'
#			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
#		else:
#			localProjectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\projectdir'
#			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

#		# reading and rewriting test project files to update their modification date

#		tstFileToModifyLst = ['testfilemover_2.py']
#		pythonFileToModifyLst = ['filemover_2.py', 'filelister_2.py']
#		docFileToModifyLst = ['doc_21.docx', 'doc_22.docx']
#		imgFileToModifyLst = ['current_state_21.jpg']
#		
#		tstFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'test' + DIR_SEP + x for x in tstFileToModifyLst]
#		pythonFilePathNameToModifyLst = [localProjectDir + DIR_SEP + x for x in pythonFileToModifyLst]
#		docFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'doc' + DIR_SEP + x for x in docFileToModifyLst]
#		imgFilePathNameToModifyLst = [localProjectDir + DIR_SEP + 'images' + DIR_SEP + x for x in imgFileToModifyLst]
#		
#		filePathNameToModifyLst = tstFilePathNameToModifyLst + pythonFilePathNameToModifyLst + docFilePathNameToModifyLst + imgFilePathNameToModifyLst
#		
#		#print(filePathNameToModifyLst)

#		for filePathName in filePathNameToModifyLst:
#			with open(filePathName, 'rb+') as f: # opening file as readwrite in binary mode
#				content = f.read()
#				f.seek(0)
#				f.write(content)
#				f.close()
#				
#		# simulating user input
#		
#		
#		# capturing program output
#		
#		stdout = sys.stdout

#		if os.name == 'posix':
#			FILE_PATH = '/sdcard/transFileCloudUnitTestOutput.txt'
#		else:
#			FILE_PATH = 'c:\\temp\\transFileCloudUnitTestOutput.txt'

#		# using a try/catch here prevent the test from failing due to the run of CommandQuit !
#		try:
#			with open(FILE_PATH, 'w') as outFile:
#				sys.stdout = outFile
#				rq.getProjectName(None)  # will eat up what has been filled in stdin using StringIO above
#		except:
#			pass

#		# now asking TransferFiles to upload the modified files
#		sys.stdin = StringIO('1')					
#		tf = TransferFiles(configFilePath=configFilePathName)
#		
#		sys.stdin = StringIO('Y')
#		tf.uploadModifiedFilesToCloud()
				
if __name__ == '__main__':
	unittest.main()
#	tst = TestDropboxAccess()
#	tst.testUploadSameFileTwice()
