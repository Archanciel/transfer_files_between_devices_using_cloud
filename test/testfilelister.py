import unittest
import os, sys, inspect, shutil


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager
from filelister import FileLister

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

class TestFileLister(unittest.TestCase):
	def testFileListerConstructor(self):
		if os.name == 'posix':
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir'
			fromDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			fromDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
		
		# deleting fromDir
		if os.path.exists(fromDir):
			shutil.rmtree(fromDir)

		# restoring fromDir from its saved version
		shutil.copytree(fromDirSaved, fromDir)

		fl = FileLister(configManager, fromDir)
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allPythonFileLst))
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allTestPythonFileLst))
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), sorted(fl.allImageFileLst))
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), sorted(fl.allDocFileLst))
		self.assertEqual(sorted(['README_1.rd']), sorted(fl.allReadmeFileLst))
		
	def testRemoveTestFilesFromPythonFilesLst(self):
		if os.name == 'posix':
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir'
			fromDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
		else:
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			fromDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'

		configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
		
		# deleting fromDir
		if os.path.exists(fromDir):
			shutil.rmtree(fromDir)

		# restoring fromDir from its saved version
		shutil.copytree(fromDirSaved, fromDir)

		fl = FileLister(configManager, fromDir)
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allPythonFileLst))
		fl.removeTestFilesFromPythonFilesLst()
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py']), sorted(fl.allPythonFileLst))
		
if __name__ == '__main__':
	unittest.main()
