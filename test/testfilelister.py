import unittest
import os, sys, inspect, shutil, datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import *
from filelister import FileLister
from constants import DIR_SEP, DATE_TIME_FORMAT


if os.name == 'posix':
	CONFIG_FILE_PATH_NAME = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'	
else:
	CONFIG_FILE_PATH_NAME = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			
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
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allPythonFileNameLst))
		self.assertEqual(sorted(['testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allTestPythonFileNameLst))
		self.assertEqual(sorted(['current_state_12.jpg', 'current_state_11.jpg']), sorted(fl.allImageFileNameLst))
		self.assertEqual(sorted(['doc_12.docx', 'doc_11.docx']), sorted(fl.allDocFileNameLst))
		self.assertEqual(sorted(['README_1.rd']), sorted(fl.allReadmeFileNameLst))
		
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
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py', 'testfilelister_1.py', 'testfilemover_1.py']), sorted(fl.allPythonFileNameLst))
		fl.removeTestFilesFromPythonFilesLst()
		self.assertEqual(sorted(['filelister_1.py', 'filemover_1.py', 'constants_1.py']), sorted(fl.allPythonFileNameLst))

	def testGetModifiedFileLst(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)
		allFileNameLst, allFilePathNameLst = fl.getModifiedFileLst('transFileCloudTestProject')

		self.assertEqual(sorted(
			['constants_2.py', 'filelister_2.py', 'filemover_2.py', 'testfilelister_2.py', 'testfilemover_2.py', 'current_state_21.jpg', 'current_state_22.jpg', 'doc_21.docx', 'doc_22.docx', 'README_2.rd']),
						 sorted(allFileNameLst))
		if os.name == 'posix':
			self.assertEqual(sorted(
				['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/constants_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/filelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/filemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/test/testfilelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/test/testfilemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/images/current_state_21.jpg', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/images/current_state_22.jpg', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/doc/doc_21.docx', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/doc/doc_22.docx', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/projectdir/README_2.rd']),
							 sorted(allFilePathNameLst))
		else:
			self.assertEqual(sorted(
				['D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\constants_2.py', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\filelister_2.py', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\filemover_2.py', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\test\\testfilelister_2.py', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\test\\testfilemover_2.py', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\images\\current_state_21.jpg', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\images\\current_state_22.jpg', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\doc\\doc_21.docx', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\doc\\doc_22.docx', 'D:\\\\Development\\\\Python\\\\trans_file_cloud\\\\test\\\\testproject_2\\\\projectdir\\README_2.rd']),
							 sorted(allFilePathNameLst))

	def testListFilesRecursively(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)
		projectDir = 'does_not_exist'
		lastSyncTimeStr = '2020-06-18 08:45:23'
		lastSyncTime = datetime.datetime.strptime(lastSyncTimeStr, DATE_TIME_FORMAT)
		self.assertRaises(NotADirectoryError, fl.listFilesRecursively, lastSyncTime, projectDir)

if __name__ == '__main__':
	unittest.main()
