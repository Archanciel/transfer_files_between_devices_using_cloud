import unittest
import os, sys, inspect, shutil, datetime, re, functools

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configmanager import *
from filelister import FileLister
from constants import DIR_SEP, DATE_TIME_FORMAT_CONFIG_FILE
			
class TestFileLister(unittest.TestCase):
	def testGetModifiedFileLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)
		allFileNameLst, allFilePathNameLst, lastSyncTimeStr = fl.getModifiedFileLst('transFileCloudTestProject')

		self.assertEqual(sorted(
			['constants_2.py', 'filelister_2.py', 'filemover_2.py', 'testfilelister_2.py', 'testfilemover_2.py', 'README_2.md']),
						 sorted(allFileNameLst))
		if os.name == 'posix':
			self.assertEqual(sorted(
				['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/constants_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/README_2.md']),
							 sorted(allFilePathNameLst))
		else:
			self.assertEqual(sorted(
				['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\constants_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\README_2.md']),
							 sorted(allFilePathNameLst))

		self.assertEqual('2020-06-15 08:45:23', lastSyncTimeStr)

	def testGetModifiedFileLst_invalid_local_dir(self):
		'''
		Tests that the getModifiedFileLst() method raises a NotADirectoryError
		if the project path specified in the transfiles.ini does not exist.
		'''
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)
		
		# project name which has an invalid (not existing) project path in the
		# transfiles.ini file
		invalidProjectName = 'transFileCloudInvalidProject'
		self.assertRaises(NotADirectoryError, fl.getModifiedFileLst, invalidProjectName)

	def testConvertWildcardExprStrToRegexpStr(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		wildchardLst = ['*Solemne*.mp3', 'test*.py', '/excldir/subdir/*.py', 'd:\\excldir\\subdir\\*.py', '/excldir/subdir/*.*', 'd:\\excldir\\subdir\\*.*']
		expectedRegexpLst = ['.*Solemne.*\.mp3\Z', 'test.*\.py\Z', '/excldir/subdir/.*\.py\Z', 'd:\\\\excldir\\\\subdir\\\\.*\.py\Z', '/excldir/subdir/.*\..*\Z', 'd:\\\\excldir\\\\subdir\\\\.*\..*\Z']

		for wildchardExpr, expectedRegexp in zip(wildchardLst, expectedRegexpLst):
			self.assertEqual(expectedRegexp, fl.convertWildcardExprStrToRegexpStr(wildchardExpr))

	def testCreateRegexpPatternLstFromWildchardExprLst(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		wildchardLst = ['*Solemne*.mp3', 'test*.py', '/excldir/subdir/*.py', 'd:\\excldir\\subdir\\*.py', '/excldir/subdir/*.*', 'd:\\excldir\\subdir\\*.*']
		expectedPatternLst = [re.compile('.*Solemne.*\.mp3\Z'),    re.compile('test.*\.py\Z'), re.compile('/excldir/subdir/.*\.py\Z'), re.compile('d:\\\\excldir\\\\subdir\\\\.*\.py\Z'), re.compile('/excldir/subdir/.*\..*\Z'), re.compile('d:\\\\excldir\\\\subdir\\\\.*\..*\Z')]

		self.assertEqual(expectedPatternLst, fl.createRegexpPatternLstFromWildchardExprLst(wildchardLst))
		
	def testExcludeFile(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

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
			projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
			projectDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)
		
		expectedAllFileNameLst = ['constants_2.py', 'filelister_2.py', 'filemover_2.py', 'README_2.md', 'testfilelister_2.py', 'testfilemover_2.py']

		if os.name == 'posix':
			expectedAllFilePathNameLst = ['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/constants_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/filemover_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/README_2.md', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilelister_2.py', '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_3/projectdir/test/testfilemover_2.py']
		else:			
			expectedAllFilePathNameLst = ['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\constants_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\filemover_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\README_2.md', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilelister_2.py', 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_3\\projectdir\\test\\testfilemover_2.py']

		excludedDirLst = []
		excludedFileTypeWildchardLst = ['*.ini', '*.tmp', '*.jpg', '*.docx']

		excludedFileTypePatternLst = fl.createRegexpPatternLstFromWildchardExprLst(excludedFileTypeWildchardLst)			
		lastSyncTime = datetime.datetime.strptime('2020-06-15 08:45:23', DATE_TIME_FORMAT_CONFIG_FILE)

		actualAllFileNameLst, actualAllFilePathNameLst = fl.getModifiedAndNotExcludedFileLst(projectDir, lastSyncTime, excludedDirLst, excludedFileTypePatternLst)
		self.assertEqual(sorted(expectedAllFileNameLst), sorted(actualAllFileNameLst))
		self.assertEqual(sorted(expectedAllFilePathNameLst), sorted(actualAllFilePathNameLst))

	def testGetFilesByOrderedTypes(self):
		if os.name == 'posix':
			configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
		else:
			configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)
		cloudFileLst = ['aa_current.jpg', 'constants_2.py', 'current_state_21.jpg', 'current_state_22.jpg', 'doc_21.docx', 'doc_22.docx', 'filelister_2.py', 'filemover_2.py', 'README_2.md', 'testfilelister_2.py', 'testfilemover_2.py']

		orderedFileTypeWildchardExprLst, fileTypeDic = fl.getFilesByOrderedTypes('transFileCloudTestProject', cloudFileLst=cloudFileLst)

		self.assertEqual(['aa*.jpg',
						  '*Solemne*.mp3',
						  'test*.py',
						  '*.mp3',
						  '*.jpg',
						  '*.docx',
						  '*.py',
						  '*.md'], orderedFileTypeWildchardExprLst)

		if os.name == 'posix':
			self.assertEqual({'*.jpg': ('/images', ['current_state_21.jpg', 'current_state_22.jpg']),
							'*.docx': ('/doc', ['doc_21.docx', 'doc_22.docx']),
							'*.md': ('', ['README_2.md']),
							'*.mp3': ('/mp3', []),
							'test*.py': ('/test', ['testfilelister_2.py', 'testfilemover_2.py']),
							'*.py': ('', ['constants_2.py', 'filelister_2.py', 'filemover_2.py']),
							'*Solemne*.mp3': ('/mp3/solemne', []),
							 'aa*.jpg': ('/images/aa', ['aa_current.jpg'])}, fileTypeDic)
		else:
			self.assertEqual({'*.jpg': ('\\images', ['current_state_21.jpg', 'current_state_22.jpg']),
							'*.docx': ('\\doc', ['doc_21.docx', 'doc_22.docx']),
							'*.md': ('', ['README_2.md']),
							'*.mp3': ('\\mp3', []),
							'test*.py': ('\\test', ['testfilelister_2.py', 'testfilemover_2.py']),
							'*.py': ('', ['constants_2.py', 'filelister_2.py', 'filemover_2.py']),
							'*Solemne*.mp3': ('\\mp3\\solemne', []),
							 'aa*.jpg': ('\\images\\aa', ['aa_current.jpg'])}, fileTypeDic)

	def testSortFilePatternDirTupleLst_2_items(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)
		
		if os.name == 'posix':
			filePatternDirTupleLst = [('*.py', ''), ('test*.py', '/test')]
			self.assertEqual([('test*.py', '/test'), ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

			filePatternDirTupleLst = [('test*.py', '/test'), ('*.py', '')]
			self.assertEqual([('test*.py', '/test'), ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))
		else:
			filePatternDirTupleLst = [('*.py', ''), ('test*.py', '\\test')]
			self.assertEqual([('test*.py', '\\test'), ('*.py', '')],
							 fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

			filePatternDirTupleLst = [('test*.py', '\\test'), ('*.py', '')]
			self.assertEqual([('test*.py', '\\test'), ('*.py', '')],
							 fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

	def testSortFilePatternDirTupleLst_2_items_one_start_With_star(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		if os.name == 'posix':
			filePatternDirTupleLst = [('*.mp3', ''), ('*Rimsky-Korsakov*.mp3', '/rim')]
			self.assertEqual([('*Rimsky-Korsakov*.mp3', '/rim'), ('*.mp3', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))
	
			filePatternDirTupleLst = [('*Rimsky-Korsakov*.mp3', '/rim'), ('*.mp3', '')]
			self.assertEqual([('*Rimsky-Korsakov*.mp3', '/rim'), ('*.mp3', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))
		else:
			filePatternDirTupleLst = [('*.mp3', ''), ('*Rimsky-Korsakov*.mp3', '\\rim')]
			self.assertEqual([('*Rimsky-Korsakov*.mp3', '\\rim'), ('*.mp3', '')],
							 fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

			filePatternDirTupleLst = [('*Rimsky-Korsakov*.mp3', '\\rim'), ('*.mp3', '')]
			self.assertEqual([('*Rimsky-Korsakov*.mp3', '\\rim'), ('*.mp3', '')],
							 fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

	def testSortFilePatternDirTupleLst_n_items(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		if os.name == 'posix':
			filePatternDirTupleLst = [('*.py', ''), ('test*.py', '/test'), ('*.jpg', '/images'), ('sub*.jpg', '/images/sub'), ('*.docx', '/doc')]
			self.assertEqual([('sub*.jpg', '/images/sub'),
							  ('test*.py', '/test'),
							  ('*.jpg', '/images'),
							  ('*.docx', '/doc'),
							  ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

			filePatternDirTupleLst = [('sub*.jpg', '/images/sub'), ('*.jpg', '/images'), ('*.docx', '/doc'), ('aa*.docx', '/doc/aa_sub_dir'), ('test*.py', '/test'), ('*.py', '')]
			self.assertEqual([('sub*.jpg', '/images/sub'),
							  ('aa*.docx', '/doc/aa_sub_dir'),
							  ('test*.py', '/test'),
							  ('*.jpg', '/images'),
							  ('*.docx', '/doc'),
							  ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))
		else:
			filePatternDirTupleLst = [('*.py', ''), ('test*.py', '\\test'), ('*.jpg', '\\images'), ('sub*.jpg', '\\images\\sub'), ('*.docx', '\\doc')]
			self.assertEqual([('sub*.jpg', '\\images\\sub'),
							  ('test*.py', '\\test'),
							  ('*.jpg', '\\images'),
							  ('*.docx', '\\doc'),
							  ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

			filePatternDirTupleLst = [('sub*.jpg', '\\images\\sub'), ('*.jpg', '\\images'), ('*.docx', '\\doc'), ('aa*.docx', '\\doc\\aa_sub_dir'), ('test*.py', '\\test'), ('*.py', '')]
			self.assertEqual([('sub*.jpg', '\\images\\sub'),
							  ('aa*.docx', '\\doc\\aa_sub_dir'),
							  ('test*.py', '\\test'),
							  ('*.jpg', '\\images'),
							  ('*.docx', '\\doc'),
							  ('*.py', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

	def testSortFilePatternDirTupleLst_n_items_one_start_With_star(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		if os.name == 'posix':
			filePatternDirTupleLst = [('test*.py', '/test'), ('*.py', ''), ('*.md', ''), ('*.docx', '/doc'), ('*.jpg', '/images'), ('sub*.jpg', '/images/sub'), ('*.mp3', '/mp3'), ('*Rimsky-Korsakov*.mp3', '/mp3/Rimsky-Korsakov')]
			self.assertEqual([('sub*.jpg', '/images/sub'),
							  ('*Rimsky-Korsakov*.mp3', '/mp3/Rimsky-Korsakov'),
							  ('test*.py', '/test'),
							  ('*.mp3', '/mp3'),
							  ('*.jpg', '/images'),
							  ('*.docx', '/doc'),
							  ('*.py', ''),
							  ('*.md', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))
		else:
			filePatternDirTupleLst = [('test*.py', '\\test'), ('*.py', ''), ('*.md', ''), ('*.docx', '\\doc'), ('*.jpg', '\\images'), ('sub*.jpg', '\\images\\sub'), ('*.mp3', '\\mp3'), ('*Rimsky-Korsakov*.mp3', '\\mp3\\Rimsky-Korsakov')]
			self.assertEqual([('sub*.jpg', '\\images\\sub'),
							  ('*Rimsky-Korsakov*.mp3', '\\mp3\\Rimsky-Korsakov'),
							  ('test*.py', '\\test'),
							  ('*.mp3', '\\mp3'),
							  ('*.jpg', '\\images'),
							  ('*.docx', '\\doc'),
							  ('*.py', ''),
							  ('*.md', '')], fl.sortFilePatternDirTupleLst(filePatternDirTupleLst))

	def testIsRootAsDirOrSubDirInExcludedDirLst(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
			excludedDirLst = ['/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir',
			 '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved']

			subDir1 = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir/fromSubDir'
			subDir2 = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir_saved/fromSubDir'
			subDir3 = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir_saved/fromSubDir'
			dir1 = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_1/fromdir'
			dir2 = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2'
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'
			excludedDirLst = ['D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir',
			 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved']

			subDir1 = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir\\fromSubDir'
			subDir2 = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir_saved\\fromSubDir'
			subDir3 = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\fromdir_saved\\fromSubDir'
			dir1 = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_1\\fromdir'
			dir2 = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2'

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		self.assertTrue(fl.isRootAsDirOrSubDirInExcludedDirLst(subDir1, excludedDirLst))
		self.assertTrue(fl.isRootAsDirOrSubDirInExcludedDirLst(subDir2, excludedDirLst))
		self.assertTrue(fl.isRootAsDirOrSubDirInExcludedDirLst(dir1, excludedDirLst))
		self.assertFalse(fl.isRootAsDirOrSubDirInExcludedDirLst(subDir3, excludedDirLst))
		self.assertFalse(fl.isRootAsDirOrSubDirInExcludedDirLst(dir2, excludedDirLst))

	def testSortDirTupleListUsingComputeMoveOrder(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
			filePatternDirDic = {'test*.py': '/test',
								 '*.py': '/',
								 '*.rd': '/',
								 '*.docx': '/doc',
								 '*.jpg': '/images',
								 'aacc*.mp3': '/aaccmp3',
								 'cc*.mp3': '/ccmp3',
								 '*.mp3': '/mp3',
								 'aa*.mp3': '/aamp3',
								 'bb*.mp3': '/bbmp3',
								 ' *Rimsky-Korsakov*.mp3': '/mp3/Rimsky Korsakov'}
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'
			filePatternDirDic = {'test*.py': '\\test',
								 '*.py': '\\',
								 '*.rd': '\\',
								 '*.docx': '\\doc',
								 '*.jpg': '\\images',
								 'aacc*.mp3': '\\aaccmp3',
								 'cc*.mp3': '\\ccmp3',
								 '*.mp3': '\\mp3',
								 'aa*.mp3': '\\aamp3',
								 'bb*.mp3': '\\bbmp3',
								 ' *Rimsky-Korsakov*.mp3': '\\mp3\\Rimsky Korsakov'}

		filePatternDirTupleLst = [item for item in filePatternDirDic.items()]

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		if os.name == 'posix':
			self.assertEqual([(' *Rimsky-Korsakov*.mp3', '/mp3/Rimsky Korsakov'), 
								('test*.py', '/test'), 
								('cc*.mp3', '/ccmp3'), 
								('bb*.mp3', '/bbmp3'), 
								('aacc*.mp3', '/aaccmp3'), 
								('aa*.mp3', '/aamp3'), 
								('*.rd', '/'), ('*.py', '/'), 
								('*.mp3', '/mp3'), 
								('*.jpg', '/images'), 
								('*.docx', '/doc')], sorted(filePatternDirTupleLst, key=functools.cmp_to_key(fl.computeMoveOrder)))
		else:
			self.assertEqual([(' *Rimsky-Korsakov*.mp3', '\\mp3\\Rimsky Korsakov'), 
								('test*.py', '\\test'), 
								('cc*.mp3', '\\ccmp3'), 
								('bb*.mp3', '\\bbmp3'), 
								('aacc*.mp3', '\\aaccmp3'), 
								('aa*.mp3', '\\aamp3'), 
								('*.rd', '\\'), ('*.py', '\\'), 
								('*.mp3', '\\mp3'), 
								('*.jpg', '\\images'), 
								('*.docx', '\\doc')], sorted(filePatternDirTupleLst, key=functools.cmp_to_key(fl.computeMoveOrder)))

	def testSortDirTupleListUsingComputeMoveOrder_empty_root_dir(self):
		if os.name == 'posix':
			configFilePathName = '/sdcard/transfiles.ini'
			filePatternDirDic = {'test*.py': '/test',
								 '*.py': '',
								 '*.rd': '',
								 '*.docx': '/doc',
								 '*.jpg': '/images',
								 'aacc*.mp3': '/aaccmp3',
								 'cc*.mp3': '/ccmp3',
								 '*.mp3': '/mp3',
								 'aa*.mp3': '/aamp3',
								 'bb*.mp3': '/bbmp3',
								 ' *Rimsky-Korsakov*.mp3': '/mp3/Rimsky Korsakov'}
		else:
			configFilePathName = 'c:\\temp\\transfiles.ini'
			filePatternDirDic = {'test*.py': '\\test',
								 '*.py': '',
								 '*.rd': '',
								 '*.docx': '\\doc',
								 '*.jpg': '\\images',
								 'aacc*.mp3': '\\aaccmp3',
								 'cc*.mp3': '\\ccmp3',
								 '*.mp3': '\\mp3',
								 'aa*.mp3': '\\aamp3',
								 'bb*.mp3': '\\bbmp3',
								 ' *Rimsky-Korsakov*.mp3': '\\mp3\\Rimsky Korsakov'}

		filePatternDirTupleLst = [item for item in filePatternDirDic.items()]

		cm = ConfigManager(configFilePathName)
		fl = FileLister(cm)

		if os.name == 'posix':
			self.assertEqual([(' *Rimsky-Korsakov*.mp3', '/mp3/Rimsky Korsakov'), 
								('test*.py', '/test'), 
								('cc*.mp3', '/ccmp3'), 
								('bb*.mp3', '/bbmp3'), 
								('aacc*.mp3', '/aaccmp3'), 
								('aa*.mp3', '/aamp3'), 
								('*.mp3', '/mp3'),
								('*.jpg', '/images'), 
								('*.docx', '/doc'),
							  	('*.rd', ''),
							  	('*.py', '')], sorted(filePatternDirTupleLst, key=functools.cmp_to_key(fl.computeMoveOrder)))
		else:
			self.assertEqual([(' *Rimsky-Korsakov*.mp3', '\\mp3\\Rimsky Korsakov'), 
								('test*.py', '\\test'), 
								('cc*.mp3', '\\ccmp3'), 
								('bb*.mp3', '\\bbmp3'), 
								('aacc*.mp3', '\\aaccmp3'), 
								('aa*.mp3', '\\aamp3'), 
								('*.mp3', '\\mp3'),
								('*.jpg', '\\images'), 
								('*.docx', '\\doc'),
								('*.rd', ''),
								('*.py', '')], sorted(filePatternDirTupleLst, key=functools.cmp_to_key(fl.computeMoveOrder)))

if __name__ == '__main__':
	unittest.main()
