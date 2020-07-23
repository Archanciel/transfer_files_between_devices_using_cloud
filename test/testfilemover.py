import unittest
import os, sys, inspect, shutil
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager
from filemover import FileMover
from filelister import FileLister

if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/test_FileMover.ini'
else:
	CONFIG_FILE_PATH_NAME = 'D:\\Development\\Python\\trans_file_cloud\\test\\test_FileMover.ini'

class TestFileMover(unittest.TestCase):
	def testMoveFilesToLocalDirs(self):
		if os.name == 'posix':
			downloadDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir'
			downloadDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
			projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/projectdir'
			projectDirEmpty = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/projectdir_empty'

			TEST_SUB_DIR = '/test'
			IMG_SUB_DIR = '/images'
			DOC_SUB_DIR = '/doc'
		else:
			# Windows
			downloadDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			downloadDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'
			projectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\projectdir'
			projectDirEmpty = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\projectdir_empty'

			TEST_SUB_DIR = '\\test'
			IMG_SUB_DIR = '\\images'
			DOC_SUB_DIR = '\\doc'

		configManager = ConfigManager(CONFIG_FILE_PATH_NAME)

		# deleting downloadDir
		if os.path.exists(downloadDir):
			shutil.rmtree(downloadDir)

		# restoring downloadDir from its saved version
		shutil.copytree(downloadDirSaved, downloadDir)

		# deleting projectDir
		if os.path.exists(projectDir):
			shutil.rmtree(projectDir)

		# restoring a directory structure only project dir (no files) from its saved empty version
		shutil.copytree(projectDirEmpty, projectDir)

		# ensuring downloadDir contains the required files
		
		fl = FileLister(configManager)
		projectName = 'transFileCloudTestProject'
		cloudFileLst = ['constants_1.py', 'current_state_11.jpg', 'current_state_12.jpg', 'doc_11.docx', 'doc_12.docx', 'filelister_1.py', 'filemover_1.py', 'README_1.md', 'testfilelister_1.py', 'testfilemover_1.py']
		_, fileTypeDic = fl.getFilesByOrderedTypes(projectName, cloudFileLst=cloudFileLst)
		
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py']), fileTypeDic['*.py'][1])
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), fileTypeDic['test*.py'][1])
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), fileTypeDic['*.jpg'][1])
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), fileTypeDic['*.docx'][1])
		self.assertEqual(sorted(['README_1.md']), fileTypeDic['*.md'][1])

		fm = FileMover(configManager, projectName)
		fm.projectDir = projectDir

		# capturing stdout into StringIO to avoid outputing in terminal
		# window while unit testing
				
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		fm.moveFilesToLocalDirs(cloudFileLst)

		sys.stdout = stdout
				
		# using FileLister to test that the expected files were correctly moved
		# to the previously empty project dir. Remember that FileLister.getFilesByOrderedTypes()
		# only works on the passed directory, not on its sub directories. For this reason,
		# several instances of FileLister are used below.

		# verifying project dir
		flp = FileLister(configManager)
		_, projectDirFileTypeDic = flp.getFilesByOrderedTypes(projectName, localDir=projectDir)
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py']), projectDirFileTypeDic['*.py'][1])
		self.assertEqual(sorted(['README_1.md']), projectDirFileTypeDic['*.md'][1])

		# verifying project test sub dir
		flt = FileLister(configManager)
		_, projectTestDirFileTypeDic = flt.getFilesByOrderedTypes(projectName, localDir=projectDir + TEST_SUB_DIR)
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), projectTestDirFileTypeDic['test*.py'][1])

		# verifying project images sub dir
		fli = FileLister(configManager)
		_, projectImagesDirFileTypeDic = fli.getFilesByOrderedTypes(projectName, localDir=projectDir + IMG_SUB_DIR)
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), projectImagesDirFileTypeDic['*.jpg'][1])

		# verifying project doc s	ub dir
		fld = FileLister(configManager)
		_, projectDocDirFileTypeDic = fld.getFilesByOrderedTypes(projectName, localDir=projectDir + DOC_SUB_DIR)
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), projectDocDirFileTypeDic['*.docx'][1])

		# testing that download is now empty
		fld = FileLister(configManager)
		_, downloadDirFileTypeDic = fld.getFilesByOrderedTypes(projectName, localDir=downloadDir)
		self.assertEqual([], downloadDirFileTypeDic['*.py'][1])
		self.assertEqual([], downloadDirFileTypeDic['test*.py'][1])
		self.assertEqual([], downloadDirFileTypeDic['*.jpg'][1])
		self.assertEqual([], downloadDirFileTypeDic['*.docx'][1])
		self.assertEqual([], downloadDirFileTypeDic['*.md'][1])

if __name__ == '__main__':
	unittest.main()
