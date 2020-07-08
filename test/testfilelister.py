import unittest
import os, sys, inspect, shutil, datetime, re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import *
from filelister import FileLister
from constants import DIR_SEP, DATE_TIME_FORMAT
			
class TestFileLister(unittest.TestCase):
	def testFileListerConstructor(self):
		if os.name == 'posix':
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir'
			fromDirSaved = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved'
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			fromDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		
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
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			fromDirSaved = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved'
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		configManager = ConfigManager(configFilePathName)
		
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
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)
		allFileNameLst, allFilePathNameLst, lastSyncTimeStr = fl.getModifiedFileLst('transFileCloudTestProject')

		self.assertEqual(sorted(
			['constants_2.py', 'filelister_2.py', 'filemover_2.py', 'testfilelister_2.py', 'testfilemover_2.py', 'README_2.rd']),
						 sorted(allFileNameLst))
		if os.name == 'posix':
			self.assertEqual(sorted(
				['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/constants_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/README_2.rd']),
							 sorted(allFilePathNameLst))
		else:
			self.assertEqual(sorted(
				['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\constants_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\README_2.rd']),
							 sorted(allFilePathNameLst))

		self.assertEqual('2020-06-15 08:45:23', lastSyncTimeStr)

	def testGetModifiedFileLst_invalid_local_dir(self):
		'''
		Tests that the getModifiedFileLst() method raises a NotADirectoryError
		if the project path specified in the transfiles.ini does not exist.
		'''
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)
		
		# project name which has an invalid (not existing) project path in the
		# transfiles.ini file
		invalidProjectName = 'transFileCloudInvalidProject'
		self.assertRaises(NotADirectoryError, fl.getModifiedFileLst, invalidProjectName)

	def testConvertWildcardExprStrToRegexpStr(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)

		wildchardLst = ['test*.py', '/excldir/subdir/*.py', 'd:\\excldir\\subdir\\*.py', '/excldir/subdir/*.*', 'd:\\excldir\\subdir\\*.*']
		expectedRegexpLst = ['test.*\.py\Z', '/excldir/subdir/.*\.py\Z', 'd:\\\\excldir\\\\subdir\\\\.*\.py\Z', '/excldir/subdir/.*\..*\Z', 'd:\\\\excldir\\\\subdir\\\\.*\..*\Z']

		for wildchardExpr, expectedRegexp in zip(wildchardLst, expectedRegexpLst):
			self.assertEqual(expectedRegexp, fl.convertWildcardExprStrToRegexpStr(wildchardExpr))

	def testCreateRegexpPatternLstFromWildchardExprLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)

		wildchardLst = ['test*.py', '/excldir/subdir/*.py', 'd:\\excldir\\subdir\\*.py', '/excldir/subdir/*.*', 'd:\\excldir\\subdir\\*.*']
		expectedPatternLst = [re.compile('test.*\.py\Z'), re.compile('/excldir/subdir/.*\.py\Z'), re.compile('d:\\\\excldir\\\\subdir\\\\.*\.py\Z'), re.compile('/excldir/subdir/.*\..*\Z'), re.compile('d:\\\\excldir\\\\subdir\\\\.*\..*\Z')]

		self.assertEqual(expectedPatternLst, fl.createRegexpPatternLstFromWildchardExprLst(wildchardLst))
		
	def testExcludeFile(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)

		excludedFileSpecLst = ['*.ini', '*.temp', 'help*.*', 'modified*', '*.pyc']
		excludedPatternLst = fl.createRegexpPatternLstFromWildchardExprLst(excludedFileSpecLst)
		
		self.assertTrue(fl.excludeFile('transfiles.ini', excludedPatternLst))
		self.assertFalse(fl.excludeFile('transfiles.py', excludedPatternLst))
		self.assertTrue(fl.excludeFile('transfiles.temp', excludedPatternLst))
		self.assertFalse(fl.excludeFile('transfiles.tmp', excludedPatternLst))
		self.assertTrue(fl.excludeFile('helpMe.txt', excludedPatternLst))
		self.assertTrue(fl.excludeFile('modified_no_type', excludedPatternLst))
		self.assertTrue(fl.excludeFile('transfiles.pyc', excludedPatternLst))	

	def testGetModifiedAndNotExcludedFileLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
			fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/fromdir'
			projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\fromdir'
			projectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm, fromDir)
		
		expectedAllFileNameLst = ['constants_2.py', 'filelister_2.py', 'filemover_2.py', 'README_2.rd', 'testfilelister_2.py', 'testfilemover_2.py']

		if os.name == 'posix':
			expectedAllFilePathNameLst = ['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/constants_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/README_2.rd', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilemover_2.py']
		else:			
			expectedAllFilePathNameLst = ['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\constants_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\README_2.rd', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilemover_2.py']

		excludedDirLst = []
		excludedFileTypeWildchardLst = ['*.ini', '*.tmp', '*.jpg', '*.docx']

		excludedFileTypePatternLst = fl.createRegexpPatternLstFromWildchardExprLst(excludedFileTypeWildchardLst)			
		lastSyncTime = datetime.datetime.strptime('2020-06-15 08:45:23', DATE_TIME_FORMAT)

		actualAllFileNameLst, actualAllFilePathNameLst = fl.getModifiedAndNotExcludedFileLst(projectDir, lastSyncTime, excludedDirLst, excludedFileTypePatternLst)
		self.assertEqual(sorted(expectedAllFileNameLst), sorted(actualAllFileNameLst))
		self.assertEqual(sorted(expectedAllFilePathNameLst), sorted(actualAllFilePathNameLst))

	def testGetFilesByOrderedTypes(self):
		pass
				
if __name__ == '__main__':
	unittest.main()
