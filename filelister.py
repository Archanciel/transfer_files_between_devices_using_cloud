import os, glob

from configmanager import ConfigManager
from constants import DIR_SEP
	
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
		
if __name__ == "__main__":
	fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/move_files/test/testproject_1/fromdir'
	fl = FileLister(fromDir)
	
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
	
	