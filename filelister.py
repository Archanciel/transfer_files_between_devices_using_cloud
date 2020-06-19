import os, glob, datetime

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
		self.allPythonFileLst = list(filter(lambda x: '.py' in x, allFileNameLst))
		self.allTestPythonFileLst = list(filter(lambda x: 'test' in x, self.allPythonFileLst))
		self.allImageFileLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		self.allDocFileLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		self.allReadmeFileLst = list(filter(lambda x: '.rd' in x, allFileNameLst))	

	def removeTestFilesFromPythonFilesLst(self):
		self.allPythonFileLst = [item for item in self.allPythonFileLst if item not in self.allTestPythonFileLst]

	def getModifiedFileLst(self, projectName):
		projectDir = self.configManager.projects[projectName][CONFIG_KEY_PROJECT_PATH]
		lastSyncTimeStr = self.configManager.projects[projectName][CONFIG_KEY_PROJECT_LAST_SYNC_TIME]
		lastSyncTime = datetime.datetime.strptime(lastSyncTimeStr, DATE_TIME_FORMAT)
		allFileNameLst = []
		allFilePathNameLst = []

		for root, dirs, files in os.walk(projectDir):
			for fileName in files:
				pathfileName = os.path.join(root, fileName)
				file_mtime = datetime.datetime.fromtimestamp(os.stat(pathfileName).st_mtime)
				if(file_mtime > lastSyncTime):
					allFileNameLst.append(fileName)
					allFilePathNameLst.append(pathfileName)
					
		allPythonFileNameLst = list(filter(lambda x: '.py' in x and '.pyc' not in x, allFileNameLst))
		allImageFileNameLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		allDocFileNameLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		allReadmeFileNameLst = list(filter(lambda x: '.rd' in x, allFileNameLst))	

		allFileNameLstReturn = allPythonFileNameLst + allImageFileNameLst + allDocFileNameLst + allReadmeFileNameLst				
					
		allPythonFilePathNameLst = list(filter(lambda x: '.py' in x and '.pyc' not in x, allFilePathNameLst))
		allImageFilePathNameLst = list(filter(lambda x: '.jpg' in x, allFilePathNameLst))
		allDocFilePathNameLst = list(filter(lambda x: '.docx' in x, allFilePathNameLst))
		allReadmeFilePathNameLst = list(filter(lambda x: '.rd' in x, allFilePathNameLst))	

		allFilePathNameLstReturn = allPythonFilePathNameLst + allImageFilePathNameLst + allDocFilePathNameLst + allReadmeFilePathNameLst
		
		return allFileNameLstReturn, allFilePathNameLstReturn				

if __name__ == "__main__":
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'

	cm = ConfigManager(configFilePathName)
	fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/testproject_2/fromdir'
	fl = FileLister(cm, fromDir)
	
	f = open("temp.txt", 'w')
	f.write('allPythonFileLst ')
	f.write(str(fl.allPythonFileLst))
	f.write('\r\nallTestPythonFileLst ')
	f.write(str(fl.allTestPythonFileLst))
	f.write('\r\nallImageFileLst ')
	f.write(str(fl.allImageFileLst))
	f.write('\r\nallDocFileLst ')
	f.write(str(fl.allDocFileLst))
	f.write('\r\nallReadmeFileLst ')
	f.write(str(fl.allReadmeFileLst))
	f.close()
	
	allFileNameLst, allFilePathNameLst = fl.getModifiedFileLst('transFileCloudProject')
	print(allFileNameLst)
	print(allFilePathNameLst)
	