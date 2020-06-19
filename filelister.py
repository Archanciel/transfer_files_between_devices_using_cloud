import os, glob, datetime, re

from configmanager import *
from constants import DIR_SEP, DATE_TIME_FORMAT
	
class FileLister:
	"""
	This class manages the lists of files which will be moved to specific
	directories
	"""
	def __init__(self, configManager, fromDir):
		"""
		FileLister constructor.

		:param fromDir: directory containing the files to list.
		"""
		self.configManager = configManager
		
		# creating the different file type lists
		allFileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(fromDir + '/*.*')]

		pattern = re.compile('\w*\.[py]*$')
		
		self.allPythonFileNameLst = [x for x in allFileNameLst if pattern.match(x)]
		self.allTestPythonFileNameLst = list(filter(lambda x: 'test' in x, self.allPythonFileNameLst))
		self.allImageFileNameLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		self.allDocFileNameLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		self.allReadmeFileNameLst = list(filter(lambda x: '.rd' in x, allFileNameLst))

	def removeTestFilesFromPythonFilesLst(self):
		self.allPythonFileNameLst = [item for item in self.allPythonFileNameLst if item not in self.allTestPythonFileNameLst]

	def getModifiedFileLst(self, projectName):
		projectDir = self.configManager.projects[projectName][CONFIG_KEY_PROJECT_PATH]
		lastSyncTimeStr = self.configManager.projects[projectName][CONFIG_KEY_PROJECT_LAST_SYNC_TIME]
		lastSyncTime = datetime.datetime.strptime(lastSyncTimeStr, DATE_TIME_FORMAT)
		allFileNameLst, allFilePathNameLst = self.listFilesRecursively(lastSyncTime, projectDir)

		pattern = re.compile('\w*\.[py]*$')
		
		allPythonFileNameLst = [ x for x in allFileNameLst if pattern.match(x) ]
		allImageFileNameLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		allDocFileNameLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		allReadmeFileNameLst = list(filter(lambda x: '.rd' in x, allFileNameLst))	

		allFileNameLstReturn = allPythonFileNameLst + allImageFileNameLst + allDocFileNameLst + allReadmeFileNameLst				
					
#		pattern = re.compile('[\w:\./]*\.[py]*$'.format(DIR_SEP))

		if os.name == 'posix':
			pattern = re.compile('[\w:\.{}]*\.[py]*$'.format(DIR_SEP))
		else:
			# since the Windows dir sep in strings are \\, the dir sep in the pattern must be \\\\ !
			pattern = re.compile('[\w:\.{}]*\.[py]*$'.format(DIR_SEP + DIR_SEP))

		allPythonFilePathNameLst = [ x for x in allFilePathNameLst if pattern.match(x) ]
		allImageFilePathNameLst = list(filter(lambda x: '.jpg' in x, allFilePathNameLst))
		allDocFilePathNameLst = list(filter(lambda x: '.docx' in x, allFilePathNameLst))
		allReadmeFilePathNameLst = list(filter(lambda x: '.rd' in x, allFilePathNameLst))	

		allFilePathNameLstReturn = allPythonFilePathNameLst + allImageFilePathNameLst + allDocFilePathNameLst + allReadmeFilePathNameLst
		
		return allFileNameLstReturn, allFilePathNameLstReturn

	def listFilesRecursively(self, lastSyncTime, projectDir):
		allFileNameLst = []
		allFilePathNameLst = []

		if not os.path.isdir(projectDir):
			raise NotADirectoryError(projectDir)

		for root, dirs, files in os.walk(projectDir):
			for fileName in files:
				pathfileName = os.path.join(root, fileName)
				file_mtime = datetime.datetime.fromtimestamp(os.stat(pathfileName).st_mtime)
				if (file_mtime > lastSyncTime):
					allFileNameLst.append(fileName)
					allFilePathNameLst.append(pathfileName)
		return allFileNameLst, allFilePathNameLst

if __name__ == "__main__":
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
		fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'
		fromDir = 'D:\\Development\\Python\\trans_file_cloud\\test\\testproject_2\\fromdir'

	cm = ConfigManager(configFilePathName)
	fl = FileLister(cm, fromDir)
	
	f = open("temp.txt", 'w')
	f.write('allPythonFileLst ')
	f.write(str(fl.allPythonFileNameLst))
	f.write('\r\nallTestPythonFileLst ')
	f.write(str(fl.allTestPythonFileNameLst))
	f.write('\r\nallImageFileLst ')
	f.write(str(fl.allImageFileNameLst))
	f.write('\r\nallDocFileLst ')
	f.write(str(fl.allDocFileNameLst))
	f.write('\r\nallReadmeFileLst ')
	f.write(str(fl.allReadmeFileNameLst))
	f.close()
	
	allFileNameLst, allFilePathNameLst = fl.getModifiedFileLst('transFileCloudTestProject')
	print(allFileNameLst)
	print(allFilePathNameLst)

	for fn in allFileNameLst:
		print(fn)

	print()

	for fpn in allFilePathNameLst:
		print(fpn)
	