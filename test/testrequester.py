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
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		projectName = rq.getProjectName(None) #will eat up what has been filled in stdin using StringIO above
 
		sys.stdin = stdin
		sys.stdout = stdout
 
		self.assertEqual('Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\n', outputCapturingString.getvalue())
		self.assertEqual('transFileCloudProject', projectName)
	
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
		sys.stdin = StringIO('0\nQ')
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		rq.getProjectName(None) #will eat up what has been filled in stdin using StringIO above
 
		sys.stdin = stdin
		sys.stdout = stdout
 
		self.assertEqual('Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\nInvalid selection. Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\n', outputCapturingString.getvalue())

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
		sys.stdin = StringIO('-1\nQ')

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		rq.getProjectName(None)  # will eat up what has been filled in stdin using StringIO above

		sys.stdin = stdin
		sys.stdout = stdout

		self.assertEqual('Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\nInvalid selection. Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\n', outputCapturingString.getvalue())

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
		sys.stdin = StringIO('10\nQ')

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		rq.getProjectName(None)  # will eat up what has been filled in stdin using StringIO above

		sys.stdin = stdin
		sys.stdout = stdout

		self.assertEqual('Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\nInvalid selection. Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\n', outputCapturingString.getvalue())
	
	def testGetProjectNameInvalidUserInput_return(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		rq = Requester(configManager)
		
		# simulating user input
		stdin = sys.stdin

		# invalid user input of return
		sys.stdin = StringIO('\n\nQ')
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		rq.getProjectName(None) #will eat up what has been filled in stdin using StringIO above
 
		sys.stdin = stdin
		sys.stdout = stdout
		self.assertEqual('Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\nInvalid selection. Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\nInvalid selection. Select project (Q to quit):\n\n1 transFileCloudTestProject\n2 transFileCloudProject\n3 cartesianAxesProject\n4 transFileCloudInvalidProject\n\n', outputCapturingString.getvalue())

if __name__ == '__main__':
	unittest.main()
	#tst = TestRequester()
	#tst.testGetProjectNameInvalidUserInput_zero()
