import datetime
import glob
import re
from pathlib import Path

from configmanager import *
from constants import DIR_SEP, DATE_TIME_FORMAT


class FileLister:
	"""
	This class manages the lists of files which will be moved to specific
	directories
	"""
	def __init__(self, configManager, downloadDir):
		"""
		FileLister constructor.

		:param downloadDir: directory containing the files to list.
		"""
		self.configManager = configManager
		
		# creating the different file type lists. Those lists are used by FileMover.moveFiles()
		allFileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(downloadDir + '/*.*')]

		pattern = re.compile('\w*\.[py]*$')

		self.allPythonFileNameLst = [x for x in allFileNameLst if pattern.match(x)]
		self.allTestPythonFileNameLst = list(filter(lambda x: 'test' in x, self.allPythonFileNameLst))
		self.allImageFileNameLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		self.allDocFileNameLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		self.allReadmeFileNameLst = list(filter(lambda x: '.rd' in x, allFileNameLst))

	def removeTestFilesFromPythonFilesLst(self):
		self.allPythonFileNameLst = [item for item in self.allPythonFileNameLst if item not in self.allTestPythonFileNameLst]

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

		return fileNameLst, filePathNameLst,lastSyncTimeStr
		#
		# pattern = re.compile('\w*\.[py]*$')
		#
		# allPythonFileNameLst = [ x for x in fileNameLst if pattern.match(x) ]
		# allImageFileNameLst = list(filter(lambda x: '.jpg' in x, fileNameLst))
		# allDocFileNameLst = list(filter(lambda x: '.docx' in x, fileNameLst))
		# allReadmeFileNameLst = list(filter(lambda x: '.rd' in x, fileNameLst))
		#
		# fileNameLstReturn = allPythonFileNameLst + allImageFileNameLst + allDocFileNameLst + allReadmeFileNameLst
		#
		# if os.name == 'posix':
		# 	pattern = re.compile('[\w:\.{}]*\.[py]*$'.format(DIR_SEP))
		# else:
		# 	# since the Windows dir sep in strings are \\, the dir sep in the pattern must be \\\\ !
		# 	pattern = re.compile('[\w:\.{}]*\.[py]*$'.format(DIR_SEP + DIR_SEP))
		#
		# allPythonFilePathNameLst = [ x for x in filePathNameLst if pattern.match(x) ]
		# allImageFilePathNameLst = list(filter(lambda x: '.jpg' in x, filePathNameLst))
		# allDocFilePathNameLst = list(filter(lambda x: '.docx' in x, filePathNameLst))
		# allReadmeFilePathNameLst = list(filter(lambda x: '.rd' in x, filePathNameLst))
		#
		# filePathNameLstReturn = allPythonFilePathNameLst + allImageFilePathNameLst + allDocFilePathNameLst + allReadmeFilePathNameLst
		#
		# return fileNameLstReturn, filePathNameLstReturn, lastSyncTimeStr

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
		if root in excludedDirLst:
			return True
			
		for dir in excludedDirLst:
			parentDir = Path(dir)
			childDir = Path(root)
			if parentDir in childDir.parents:
				return True

		return False

	def excludeFile(self, fileName, excludedFileNamePatternLst):
		for pattern in excludedFileNamePatternLst:
			if pattern.match(fileName):
				return True
				
		return False		
	
	def createRegexpPatternLstFromWildchardExprLst(self, excludedFileTypeWildchardLst):
		regexpPatternLst = []
		
		for fileTypeWildchardExpr in excludedFileTypeWildchardLst:
			regexpStr = self.convertWildcardExprStrToRegexpStr(fileTypeWildchardExpr)
			regexpPatternLst.append(re.compile(regexpStr))
			
		return regexpPatternLst
			
	def convertWildcardExprStrToRegexpStr(self, wildcardExpression):
		regexpStr = wildcardExpression.replace("\\", "\\\\")
		#regexpStr = wildcardExpression.replace("\", "\\")
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
	fl = FileLister(cm, fromDir)
	
	if os.name == 'posix':
		FILE_PATH = '/sdcard/transfiles_debug.txt'
	else:
		FILE_PATH = 'c:\\temp\\transfiles_debug.txt'
		
	import sys
	stdout = sys.stdout

	# using a try/catch here prevent the test from failing  due to the run of CommandQuit !
	try:
		with open(FILE_PATH, 'w') as outFile:
			sys.stdout = outFile
			fl.getModifiedFileLst('transFileCloudProject')
	except:
		pass

	outFile.close()
	sys.stdout = stdout
	
	
	
#	f = open("temp.txt", 'w')
#	f.write('allPythonFileLst ')
#	f.write(str(fl.allPythonFileNameLst))
#	f.write('\r\nallTestPythonFileLst ')
#	f.write(str(fl.allTestPythonFileNameLst))
#	f.write('\r\nallImageFileLst ')
#	f.write(str(fl.allImageFileNameLst))
#	f.write('\r\nallDocFileLst ')
#	f.write(str(fl.allDocFileNameLst))
#	f.write('\r\nallReadmeFileLst ')
#	f.write(str(fl.allReadmeFileNameLst))
#	f.close()
#	
#	fileNameLst, filePathNameLst, lastSyncTimeStr = fl.getModifiedFileLst('transFileCloudTestProject')
#	print(fileNameLst)
#	print(filePathNameLst)

#	for fn in fileNameLst:
#		print(fn)

#	print()

#	for fpn in filePathNameLst:
#		print(fpn)
#	
#	print(lastSyncTimeStr)