import datetime
import re
from pathlib import Path
import functools

from configmanager import *
from constants import DIR_SEP, DATE_TIME_FORMAT_CONFIG_FILE


class FileLister:
	"""
	This class manages the lists of files which will either be uploaded to the 
	cloud or be moved from the download directory to specific directories by the 
	FileMover class.
	"""
	def __init__(self, configManager):
		"""
		FileLister constructor.
		
		@param configManager: ConfigManager giving access to the local configuration
							  file data
		"""
		self.configManager = configManager

	def getModifiedFileLst(self, projectName):
		"""
		This method controls the listing of the files whose modification date is
		after the last synch time date stored in the local configuration file.
		
		Only files which are not in excluded dirs or whose name does not match
		an exclusion pattern, both criteria defined in the local configuration
		file, will be included in the returned list.
		
		@param projectName: project name as defined in the local configuration
							file
			
		@return: list of modified and not excluded file names
				 list of modified and not excluded file path names
				 lastSyncTimeStr as obtained from the config manager. This
				 is only useful to avoid reasking this information
				 in the caller of the method !
		"""
		projectDir = self.configManager.getProjectLocalDir(projectName)
		lastSyncTimeStr = self.configManager.getLastSynchTime(projectName)
		lastSyncTime = datetime.datetime.strptime(lastSyncTimeStr, DATE_TIME_FORMAT_CONFIG_FILE)

		if not os.path.isdir(projectDir):
			raise NotADirectoryError(projectDir)

		excludedDirLst = self.configManager.getExcludedDirLst(projectName)
		excludedFileTypeWildchardLst = self.configManager.getExcludedFileTypeWildchardLst(projectName)
		excludedFileTypePatternLst = self.createRegexpPatternLstFromWildchardExprLst(excludedFileTypeWildchardLst)

		fileNameLst, filePathNameLst = self.getModifiedAndNotExcludedFileLst(projectDir, lastSyncTime, excludedDirLst, excludedFileTypePatternLst)

		return fileNameLst, filePathNameLst, lastSyncTimeStr
	
	def createRegexpPatternLstFromWildchardExprLst(self, excludedFileTypeWildchardLst):
		"""
		Returns a list of compiled regexp pattern corresponding to the wildchard
		file name patterns specified in the project upload exclude filePattern
		sub-section as defined in the local configuration file.
		
		@param excludedFileTypeWildchardLst: list containing the wildchard
											 file name patterns specified in the 
											 project upload exclude filePattern
										 	 sub-section as defined in the local
										 	 configuration file
										 	
		@return: a list of compiled regexp pattern corresponding to the passed
				 excludedFileTypeWildchardLst:
		"""
		regexpPatternLst = []
		
		for fileTypeWildchardExpr in excludedFileTypeWildchardLst:
			regexpStr = self.convertWildcardExprStrToRegexpStr(fileTypeWildchardExpr)
			regexpPatternLst.append(re.compile(regexpStr))
			
		return regexpPatternLst
			
	def convertWildcardExprStrToRegexpStr(self, wildcardExpression):
		"""
		Converts a passed wildcardExpression specified in the project upload 
		exclude filePattern sub-section as defined in the local configuration 
		file to a regexp conform regexp expression. See the examples
		below ...
		
		'test*.py' --> 'test.*\.py\Z'
		'/excldir/subdir/*.py' --> /excldir/subdir/.*\.py\Z'
		'd:\\excldir\\subdir\\*.py' --> 'd:\\\\excldir\\\\subdir\\\\.*\.py\Z'
		'/excldir/subdir/*.*' --> /excldir/subdir/.*\..*\Z'
		'd:\\excldir\\subdir\\*.*' --> 'd:\\\\excldir\\\\subdir\\\\.*\..*\Z'
		 
		@param wildcardExpression: expression specified in the project upload 
								   exclude filePattern sub-section
								   
		@return: corresponding regexp conform expression
		"""
		regexpStr = wildcardExpression.replace("\\", "\\\\")
		regexpStr = regexpStr.replace(".", "\.")
		regexpStr = regexpStr.replace("*", ".*")
		regexpStr += "\Z"
	
		# no effect !
		# regexpStr = "\A" + regexpStr
	
		return regexpStr

	def getModifiedAndNotExcludedFileLst(self, projectDir, lastSyncTime, excludedDirLst, excludedFileNamePatternLst):
		"""
		Returns two lists, one containing file names only, the other containing
		corresponding file path names. The returned files satisfy three
		constraints:
		
			1/ they are not in any of the passed excluded dir list
			2/ their name does not match the passed excluded file name pattern
			   list
			3/ their modification time is after the passed last synch time
			
		@param projectDir: local project dir containing the modified files
		@param lastSyncTime: obtained as string from the local config file
		@param excludedDirLst: obtained from the local config file
		@param excludedFileNamePatternLst: obtained from the local config file

		@return: list of modified and not excluded file names
				 list of modified and not excluded file path names
		"""
		fileNameLst = []
		filePathNameLst = []

		for root, dirs, files in os.walk(projectDir):
			if self.isRootAsDirOrSubDirInExcludedDirLst(root, excludedDirLst):
				continue

			for fileName in files:
				if self.excludeFile(fileName, excludedFileNamePatternLst):
					continue

				pathfileName = os.path.join(root, fileName)
				file_mtime = datetime.datetime.fromtimestamp(os.stat(pathfileName).st_mtime)
				if (file_mtime > lastSyncTime):
					fileNameLst.append(fileName)
					filePathNameLst.append(pathfileName)

		return fileNameLst, filePathNameLst

	def isRootAsDirOrSubDirInExcludedDirLst(self, subDir, excludedDirLst):
		"""
		Returns True if the passed subDir is listed in the passed excludedDirLst
		or if it is a sub dir of one of the dir listed in excludedDirLst.

		Typically, the method will be useful to exclude the .git directory and all
		its sub directories.

		@param subDir: directory to test for exclusion
		@param excludedDirLst: list of dirs to exclude as specified in the project
							   upload exclude directories sub-section defined
							   the local config file
							   
		@return: True or False
		"""
		if subDir in excludedDirLst:
			return True
			
		subDirPath = Path(subDir)
			
		for exclDir in excludedDirLst:
			exclDirPath = Path(exclDir)
			
			if exclDirPath in subDirPath.parents:
				return True

		return False

	def excludeFile(self, fileName, excludedFileNamePatternLst):
		"""
		Returns True if the passed fileName is matched by one of the regexp
		pattern contained in the passed excludedFileNamePatternLst.
		
		@param fileName: file name to test for exclusion
		@param excludedFileNamePatternLst: list of compiled regexp pattern
			   corresponding to the passed excludedFileTypeWildchardLst

		@return: True if the passed file name is matched by one of the passed
				 compiled pattern
		"""
		for pattern in excludedFileNamePatternLst:
			if pattern.match(fileName):
				return True
				
		return False		

	def getFilesByOrderedTypes(self, projectName, cloudFileLst):
		"""
		This method handles one of the key functionality of the TransferFiles
		utility. It returns two data structures. The first one is an ordered
		list of wildchard file patterns. The list is ordered so that the file
		pattern to handle first are positioned in the list before the more
		general file pattern.

		Lets take the example of 'test*.py' which is positioned before the more
		general pattern '*.py'. This means that the files whose name starts with
		'test' wiLl be moved from the download dir to their destination path 
		before the other '*.py' files. If this order was not applied, the unit 
		test Python files whose name start with 'test' would be moved from the 
		download dir to the project path root dir instead of being moved to the
		/test project sub-dir.

		Same remark for the 'aa*.jpg' files which would be moved from the 
		download dir to the /images project sub-dir instead of being moved to 
		the /images/aa project sub-dir.

		The second data structure is a dictionary whose key is the wildchard 
		file pattern listed in the first data structure and the value is a 
		tuple of two elements: the first one is the project dir or sub-dir 
		destination for this file name pattern and the second element is a
		list of files corresponding to the file pattern and contained in the
		download dir.

		The FileMover class will use those two data structures to move in the
		adequate order to their correct local destination dir the files
		downloaded from the cloud and contained in the download dir.
		
		Since the download dir may contain files matching the wildchard file
		pattern but which were not downloaded from the cloud, the passed
		cloudFileLst is used instead of the content of the download dir
		in order to populate second element of the tuple value in the returned
		dictionary.
		
		@param cloudFileLst: list of files downloaded from the cloud to the 
							 download dir which must be moved to their 
							 destination dir

		@return orderedTypeLst example: see below
		@return fileTypeDic example: see below

		Example of returned data structures for project 'transFileCloudTestProject'
		and downloadDir '/test/testproject_2/fromdir':

			['test*.py', 'aa*.jpg', '*.jpg', '*.docx', '*.py', '*.rd']
			{'*.jpg': ('/images', ['current_state_21.jpg', 'current_state_22.jpg']),
			'*.docx': ('/doc', ['doc_21.docx', 'doc_22.docx']),
			'*.rd': ('/', ['README_2.rd']),
			'aa*.jpg': ('/images/diraa', ['aa_current.jpg']),
			'test*.py': ('/test', ['testfilelister_2.py', 'testfilemover_2.py']),
			'*.py': ('/', ['constants_2.py', 'filelister_2.py', 'filemover_2.py'])}, fileTypeDic)
		"""
		filePatternDirDic = self.configManager.getFilePatternLocalDestinationDic(projectName)

		# converting the file pattern dir dictionary to a list of (key, value)
		# tuples in order to then sort the tuples based on the key tuple element.
		#
		# Ex:
		# filePatternDirTupleLst = {'test*.py': '/test', '*.py': '/'} -->
		# filePatternDirTupleSortedLst = [('test*.py', '/test'), ('*.py', '/')]

		filePatternDirTupleLst = [item for item in filePatternDirDic.items()]
		filePatternDirTupleSortedLst = self.sortFilePatternDirTupleLst(filePatternDirTupleLst)

		# extracting the tuple key element only in a key ordered list (first
		# returned data structure)

		orderedFileTypeWildchardExprLst = [x[0] for x in filePatternDirTupleSortedLst]

		# now building the second returned data structure), the file type
		# dictionary

		fileTypeDic = {}

		for fileTypeWildchardExpr in orderedFileTypeWildchardExprLst:
			regexpStr = self.convertWildcardExprStrToRegexpStr(fileTypeWildchardExpr)
			regexpPattern = re.compile(regexpStr)
			matchingFileNameLst = [x for x in cloudFileLst if regexpPattern.match(x)]
			matchingFileNameLst.sort()
			fileTypeDic[fileTypeWildchardExpr] = (filePatternDirDic[fileTypeWildchardExpr], matchingFileNameLst)

			# removing the files matched by the more specific pattern from
			# the allFileNameLst so that are not "moved" twice, once in the
			# more specific dir and once in the more general dir ...
			cloudFileLst = [x for x in cloudFileLst if x not in matchingFileNameLst]

		return orderedFileTypeWildchardExprLst, fileTypeDic
	
	def sortFilePatternDirTupleLst(self, filePatternDirTupleLst):
		"""
		This method return the filePatternDirTupleLst input tuple list reversely
		sorted according to the first tuple element, which is the file wildchard
		pattern. So, if we have two patterns like '*.py' and 'test*.py', 
		'test*.py' will be ordered before the more general pattern '*.py'. The
		effect is that the files destined to the more specific directory
		will be moved to this directory before the files destined to the
		more general directory. This is required since the more general pattern
		includes files matched by the more specific pattern.
		
		@param filePatternDirTupleLst example:
			[('*.py', '/'), ('test*.py', '/test'), ('*.jpg', '/images'), ('sub*.jpg', '/images/sub'), ('*.docx', '/doc')]

		@return value example:
			[('test*.py', '/test'),  ('sub*.jpg', '/images/sub'),  ('*.jpg', '/images'),  ('*.docx', '/doc'),  ('*.py', '/')]
		"""
		return sorted(filePatternDirTupleLst, key=functools.cmp_to_key(self.computeMoveOrder))

	def computeMoveOrder(self, typeTupleOne, typeTupleTwo):
		subDirNoOne = len(typeTupleOne[1].split(DIR_SEP))
		subDirNoTwo = len(typeTupleTwo[1].split(DIR_SEP))

		if subDirNoOne < subDirNoTwo:
			return 1
		elif subDirNoOne > subDirNoTwo:
			return -1
		else:
			wildchardOne = typeTupleOne[0]
			wildchardTwo = typeTupleTwo[0]
		
			if wildchardOne < wildchardTwo:
				return 1
			elif wildchardOne > wildchardTwo:
				return -1
			else:
				return 0
