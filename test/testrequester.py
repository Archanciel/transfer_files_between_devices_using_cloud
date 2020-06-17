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
		
		stdout = sys.stdout
		
		if os.name == 'posix':
			FILE_PATH = '/sdcard/transFileCloudUnitTestOutput.txt'
		else:
			FILE_PATH = 'c:\\temp\\transFileCloudUnitTestOutput.txt'

		projectName = ''

		# using a try/catch here prevent the test from failing  due to the run of CommandQuit !
		try:
			with open(FILE_PATH, 'w') as outFile:
				sys.stdout = outFile
				projectName = rq.getProjectName(None) #will eat up what has been filled in stdin using StringIO above
		except:
			pass
 
		sys.stdin = stdin
		sys.stdout = stdout
 
		with open(FILE_PATH, 'r') as inFile:
			contentList = inFile.readlines()
			self.assertEqual(['Select project:\n', '\n', '1 transFileCloudTestProject\n', '2 transFileCloudProject\n',
			 '3 cartesianAxesProject\n', '\n'], contentList)

		self.assertEqual('transFileCloudProject', projectName)
		
		sys.stdin = stdin
	
	def testGetProjectNameInvalidUserInput_zero(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)
		
		# simulating user input
		stdin = sys.stdin

		# invalid user input of o
		sys.stdin = StringIO('0')
		
		stdout = sys.stdout
		
		if os.name == 'posix':
			FILE_PATH = '/sdcard/transFileCloudUnitTestOutput.txt'
		else:
			FILE_PATH = 'c:\\temp\\transFileCloudUnitTestOutput.txt'

		# using a try/catch here prevent the test from failing  due to the run of CommandQuit !
		try:
			with open(FILE_PATH, 'w') as outFile:
				sys.stdout = outFile
				rq.getProjectName(None) #will eat up what has been filled in stdin using StringIO above
		except:
			pass
 
		sys.stdin = stdin
		sys.stdout = stdout
 
		with open(FILE_PATH, 'r') as inFile:
			contentList = inFile.readlines()
			self.assertEqual(['Select project:\n', '\n', '1 transFileCloudTestProject\n', '2 transFileCloudProject\n',
							  '3 cartesianAxesProject\n', '\n', 'Invalid selection. Select project:\n', '\n',
							  '1 transFileCloudTestProject\n', '2 transFileCloudProject\n', '3 cartesianAxesProject\n',
							  '\n'], contentList)

	def testGetProjectNameInvalidUserInput_minus_one(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)

		# simulating user input
		stdin = sys.stdin

		# invalid user input of -1
		sys.stdin = StringIO('-1')

		stdout = sys.stdout

		if os.name == 'posix':
			FILE_PATH = '/sdcard/transFileCloudUnitTestOutput.txt'
		else:
			FILE_PATH = 'c:\\temp\\transFileCloudUnitTestOutput.txt'

		# using a try/catch here prevent the test from failing  due to the run of CommandQuit !
		try:
			with open(FILE_PATH, 'w') as outFile:
				sys.stdout = outFile
				rq.getProjectName(None)  # will eat up what has been filled in stdin using StringIO above
		except:
			pass

		sys.stdin = stdin
		sys.stdout = stdout

		with open(FILE_PATH, 'r') as inFile:
			contentList = inFile.readlines()
			self.assertEqual(['Select project:\n', '\n', '1 transFileCloudTestProject\n', '2 transFileCloudProject\n',
							  '3 cartesianAxesProject\n', '\n', 'Invalid selection. Select project:\n', '\n',
							  '1 transFileCloudTestProject\n', '2 transFileCloudProject\n', '3 cartesianAxesProject\n',
							  '\n'], contentList)

	def testGetProjectNameInvalidUserInput_exeed_choice_number(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)

		# simulating user input
		stdin = sys.stdin

		# invalid user input of 8
		sys.stdin = StringIO('10')

		stdout = sys.stdout

		if os.name == 'posix':
			FILE_PATH = '/sdcard/transFileCloudUnitTestOutput.txt'
		else:
			FILE_PATH = 'c:\\temp\\transFileCloudUnitTestOutput.txt'

		# using a try/catch here prevent the test from failing  due to the run of CommandQuit !
		try:
			with open(FILE_PATH, 'w') as outFile:
				sys.stdout = outFile
				rq.getProjectName(None)  # will eat up what has been filled in stdin using StringIO above
		except:
			pass

		sys.stdin = stdin
		sys.stdout = stdout

		with open(FILE_PATH, 'r') as inFile:
			contentList = inFile.readlines()
			self.assertEqual(['Select project:\n', '\n', '1 transFileCloudTestProject\n', '2 transFileCloudProject\n',
							  '3 cartesianAxesProject\n', '\n', 'Invalid selection. Select project:\n', '\n',
							  '1 transFileCloudTestProject\n', '2 transFileCloudProject\n', '3 cartesianAxesProject\n',
							  '\n'], contentList)

if __name__ == '__main__':
	unittest.main()
