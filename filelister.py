import datetime
import glob
import re
from pathlib import Path
import functools

from configmanager import *
from constants import DIR_SEP, DATE_TIME_FORMAT


class FileLister:
	"""
	This class manages the lists of files which will be moved to specific
	directories
	"""
	def __init__(self, configManager):
		"""
		FileLister constructor.
		"""
		self.configManager = configManager

	def getFilesByOrderedTypes(self, projectName, downloadDir):
		"""
		This method handles one of the key functionality of the TransferFiles 
		utility. It returns two data structures. The first one is an ordered
		list of wildchard file patterns. The list is ordered so that the file
		pattern to handle first are positioned in the list before the more 
		general file pattern.
		
		Lets take the example of 'test*.py' which is positioned before the more
		general pattern '*.py'. This means that the files whose name starts with
		'test' wiLl be moved from the download dir to their destination path before 
		the other '*.py' files. If this order was not available, unit test Python 
		files whose name start with 'test' would be moved from the download dir to
		the project path root dir instead of being moved to the /test project 
		sub-dir.
		
		Same remark for the 'aa*.jpg' files which would be moved from the download
		dir to the /images project sub-dir instead of being moved to the
		/images/aa project sub-dir.
		
		The second data structure is a dictionary whose key is the wildchard file 
		pattern listed in the first data structure and the value is a tuple of two
		elements: the first one is the project dir or sub-dir destination for this
		file nàme pattern and the second element is a liet of files corresppnding
		to the file pattern and contained in the download dir.
		
		The FileMover class will use those two data etructure to move in the
		adequate order the files contained in the download dir to their correct
		local destination dir.
		
		@orderedTypeLst example: see below
		
		@fileTypeDic example: see below
		
		Example of returned data structures for project 'transFileCloudTestProject'
		and downloadDir '/test/testproject_2/fromdir':
			
			['test*.py', 'aa*.jpg', '*.jpg', '*.docx', '*.py', '*.rd']

			{'*.jpg': ('/images', ['current_state_21.jpg', 'current_state_22.jpg']), 
			'*.docx': ('/doc', ['doc_21.docx', 'doc_22.docx']),
			'*.rd': ('/', ['README_2.rd']),
			'aa*.jpg': ('/images/aa', ['aa_current.jpg']),
			'test*.py': ('/test', ['testfilelister_2.py', 'testfilemover_2.py']),
			'*.py': ('/', ['constants_2.py', 'filelister_2.py', 'filemover_2.py'])}, fileTypeDic)
		"""
		filePatternDirDic = self.configManager.getFilePatternLocalDestinationDic(projectName)
		
		# converting the file pattern dir dictionary to a list of (key, value)
		# tuples in order to then sort the tuples.
		#
		# Ex: {'test*.py': '/test', '*.py': '/'} --> [('test*.py', '/test'), ('*.py', '/')]
		filePatternDirTupleLst = [item for item in filePatternDirDic.items()]
		filePatternDirTupleSortedLst = self.sortFilePatternDirTupleLst(filePatternDirTupleLst)
		orderedFileTypeWildchardExprLst = [x[0] for x in filePatternDirTupleSortedLst]
		allFileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + DIR_SEP + '*.*')]
		fileTypeDic = {}
		
		for fileTypeWildchardExpr in orderedFileTypeWildchardExprLst:
			regexpStr = self.convertWildcardExprStrToRegexpStr(fileTypeWildchardExpr)
			regexpPattern = re.compile(regexpStr)
			matchingFileNameLst = [x for x in allFileNameLst if regexpPattern.match(x)]
			matchingFileNameLst.sort()
			fileTypeDic[fileTypeWildchardExpr] = (filePatternDirDic[fileTypeWildchardExpr], matchingFileNameLst)
			allFileNameLst = [x for x in allFileNameLst if x not in matchingFileNameLst]			

		return orderedFileTypeWildchardExprLst, fileTypeDic
	
	def sortFilePatternDirTupleLst(self, filePatternDirTupleLst):
		"""

		@param filePatternDirTupleLst:
		@return:
		"""
		return sorted(filePatternDirTupleLst, key=lambda tup: tup[1], reverse=True)

	def getModifiedFileLst(self, projectName):
		"""

		@param projectName:
		@return:
		"""
		projectDir = self.configManager.getProjectLocalDir(projectName)
		lastSyncTimeStr = self.configManager.getLastSynchTime(projectName)
		lastSyncTime = datetime.datetime.strptime(lastSyncTimeStr, DATE_TIME_FORMAT)

		if not os.path.isdir(projectDir):
			raise NotADirectoryError(projectDir)

		excludedDirLst = self.configManager.getExcludedDirLst(projectName)
		excludedFileTypeWildchardLst = self.configManager.getExcludedFileTypeWildchardLst(projectName)
		excludedFileTypePatternLst = self.createRegexpPatternLstFromWildchardExprLst(excludedFileTypeWildchardLst)

		fileNameLst, filePathNameLst = self.getModifiedAndNotExcludedFileLst(projectDir, lastSyncTime, excludedDirLst, excludedFileTypePatternLst)

		return fileNameLst, filePathNameLst, lastSyncTimeStr

	def getModifiedAndNotExcludedFileLst(self, projectDir, lastSyncTime, excludedDirLst, excludedFileNamePatternLst):
		"""
		Returns two lists, one containing file names only, the other containing
		corresponding file path names. The returned files satisfy three
		constraints:
		
			1/ they are not in any of the passed excluded dir list
			2/ their name does not match the passed excluded file name pattern
			   list
			3/ their modification time is after the passed last synch time
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

	def isRootAsDirOrSubDirInExcludedDirLst(self, root, excludedDirLst):
		"""

		@param root:
		@param excludedDirLst:
		@return:
		"""
		if root in excludedDirLst:
			return True
			
		for dir in excludedDirLst:
			parentDir = Path(dir)
			childDir = Path(root)
			if parentDir in childDir.parents:
				return True

		return False

	def excludeFile(self, fileName, excludedFileNamePatternLst):
		"""

		@param fileName:
		@param excludedFileNamePatternLst:
		@return:
		"""
		for pattern in excludedFileNamePatternLst:
			if pattern.match(fileName):
				return True
				
		return False		
	
	def createRegexpPatternLstFromWildchardExprLst(self, excludedFileTypeWildchardLst):
		"""

		@param excludedFileTypeWildchardLst:
		@return:
		"""
		regexpPatternLst = []
		
		for fileTypeWildchardExpr in excludedFileTypeWildchardLst:
			regexpStr = self.convertWildcardExprStrToRegexpStr(fileTypeWildchardExpr)
			regexpPatternLst.append(re.compile(regexpStr))
			
		return regexpPatternLst
			
	def convertWildcardExprStrToRegexpStr(self, wildcardExpression):
		"""

		@param wildcardExpression:
		@return:
		"""
		regexpStr = wildcardExpression.replace("\\", "\\\\")
		regexpStr = regexpStr.replace(".", "\.")
		regexpStr = regexpStr.replace("*", ".*")
		regexpStr += "\Z"
	
		# no effect !
		# regexpStr = "\A" + regexpStr
	
		return regexpStr
			
	
if __name__ == "__main__":
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
		fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'
		fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\fromdir'

	cm = ConfigManager(configFilePathName)
	fl = FileLister(cm)
	
	orderedFileTypeWildchardExprLst, fileTypeDic = fl.getFilesByOrderedTypes('transFileCloudTestProject', fromDir)
	
	print(orderedFileTypeWildchardExprLst)
	print(fileTypeDic)