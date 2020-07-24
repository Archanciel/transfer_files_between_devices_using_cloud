import unittest
import os, sys, inspect, shutil, glob
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import ConfigManager
from filemover import FileMover
from filelister import FileLister
from constants import DIR_SEP

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

		# purging downloadDir
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

		if os.name == 'posix':
			self.assertEqual([
								 'moving test/testproject_1/fromdir/testfilelister_1.py to testproject_1/projectdir/test/testfilelister_1.py',
								 'moving test/testproject_1/fromdir/testfilemover_1.py to testproject_1/projectdir/test/testfilemover_1.py',
								 'moving test/testproject_1/fromdir/current_state_11.jpg to testproject_1/projectdir/images/current_state_11.jpg',
								 'moving test/testproject_1/fromdir/current_state_12.jpg to testproject_1/projectdir/images/current_state_12.jpg',
								 'moving test/testproject_1/fromdir/doc_11.docx to testproject_1/projectdir/doc/doc_11.docx',
								 'moving test/testproject_1/fromdir/doc_12.docx to testproject_1/projectdir/doc/doc_12.docx',
								 'moving test/testproject_1/fromdir/constants_1.py to test/testproject_1/projectdir/constants_1.py',
								 'moving test/testproject_1/fromdir/filelister_1.py to test/testproject_1/projectdir/filelister_1.py',
								 'moving test/testproject_1/fromdir/filemover_1.py to test/testproject_1/projectdir/filemover_1.py',
								 'moving test/testproject_1/fromdir/README_1.md to test/testproject_1/projectdir/README_1.md',
								 ''],
							 outputCapturingString.getvalue().split('\n'))
		else:
			self.assertEqual(['moving test\\testproject_1\\fromdir\\testfilelister_1.py to testproject_1\\projectdir\\test\\testfilelister_1.py',
							  'moving test\\testproject_1\\fromdir\\testfilemover_1.py to testproject_1\\projectdir\\test\\testfilemover_1.py',
							  'moving test\\testproject_1\\fromdir\\current_state_11.jpg to testproject_1\\projectdir\\images\\current_state_11.jpg',
							  'moving test\\testproject_1\\fromdir\\current_state_12.jpg to testproject_1\\projectdir\\images\\current_state_12.jpg',
							  'moving test\\testproject_1\\fromdir\\doc_11.docx to testproject_1\\projectdir\\doc\\doc_11.docx',
							  'moving test\\testproject_1\\fromdir\\doc_12.docx to testproject_1\\projectdir\\doc\\doc_12.docx',
							  'moving test\\testproject_1\\fromdir\\constants_1.py to test\\testproject_1\\projectdir\\constants_1.py',
							  'moving test\\testproject_1\\fromdir\\filelister_1.py to test\\testproject_1\\projectdir\\filelister_1.py',
							  'moving test\\testproject_1\\fromdir\\filemover_1.py to test\\testproject_1\\projectdir\\filemover_1.py',
							  'moving test\\testproject_1\\fromdir\\README_1.md to test\\testproject_1\\projectdir\\README_1.md', ''],
							 outputCapturingString.getvalue().split('\n'))

		# verifying project dir
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(projectDir + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'README_1.md']), sorted(fileNameLst))

		# verifying project test sub dir
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(projectDir + TEST_SUB_DIR + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), sorted(fileNameLst))

		# verifying project images sub dir
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(projectDir + IMG_SUB_DIR + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), sorted(fileNameLst))

		# verifying project doc s	ub dir
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(projectDir + DOC_SUB_DIR + DIR_SEP + '*.*')]
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), sorted(fileNameLst))

		# testing that download is now empty
		fileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		self.assertEqual([], fileNameLst)

if __name__ == '__main__':
	unittest.main()
