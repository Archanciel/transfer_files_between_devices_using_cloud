import unittest
import os, sys, inspect, shutil

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager
from filemover import FileMover
from filelister import FileLister
from constants import *

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
else:
	CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

class TestFileMover(unittest.TestCase):
	def testMoveFiles(self):
		if os.name == 'posix':
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/move_files/test/testproject_1/fromdir'
			fromDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/move_files/test/testproject_1/fromdir_saved'
			projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/move_files/test/testproject_1/projectdir'
			projectDirEmpty = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/move_files/test/testproject_1/projectdir_empty'
		else:
			fromDir = 'D:\\Development\\Python\\move_files\\test\\testproject_1\\fromdir'
			fromDirSaved = 'D:\\Development\\Python\\move_files\\test\\testproject_1\\fromdir_saved'
			projectDir = 'D:\\Development\\Python\\move_files\\test\\testproject_1\\projectdir'
			projectDirEmpty = 'D:\\Development\\Python\\move_files\\test\\testproject_1\\projectdir_empty'

		configManager = ConfigManager(CONFIG_FILE_PATH_NAME)

		# deleting fromDir
		if os.path.exists(fromDir):
			shutil.rmtree(fromDir)

		# restoring fromDir from its saved version
		shutil.copytree(fromDirSaved, fromDir)

		# deleting projectDir
		if os.path.exists(projectDir):
			shutil.rmtree(projectDir)

		# restoring a directory structure only project dir (no files) from its saved empty version
		shutil.copytree(projectDirEmpty, projectDir)

		# ensuring fromDir contains the required files
		fl = FileLister(configManager, fromDir)
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allPythonFileLst))
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allTestPythonFileLst))
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), sorted(fl.allImageFileLst))
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), sorted(fl.allDocFileLst))
		self.assertEqual(sorted(['README_1.rd']), sorted(fl.allReadmeFileLst))
		
		fm = FileMover(configManager, fromDir, projectDir)
		fm.moveFiles()
		
		# using FileLister to test that the expected files were correctly moved
		flp = FileLister(configManager, projectDir)
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py']), sorted(flp.allPythonFileLst))
		self.assertEqual(sorted(['README_1.rd']), sorted(flp.allReadmeFileLst))

		flt = FileLister(configManager, projectDir + TEST_SUB_DIR)
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), sorted(flt.allTestPythonFileLst))

		fli = FileLister(configManager, projectDir + IMG_SUB_DIR)
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), sorted(fli.allImageFileLst))

		fld = FileLister(configManager, projectDir + DOC_SUB_DIR)
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), sorted(fld.allDocFileLst))

		# testing that fromDir is now empty
		flf = FileLister(configManager, fromDir)
		self.assertEqual([], flf.allPythonFileLst)
		self.assertEqual([], flf.allTestPythonFileLst)
		self.assertEqual([], flf.allImageFileLst)
		self.assertEqual([], flf.allDocFileLst)
		self.assertEqual([], flf.allReadmeFileLst)
		
if __name__ == '__main__':
	unittest.main()
