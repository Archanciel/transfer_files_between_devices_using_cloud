import os, glob

from constants import SRC_DIR
from constants import DIR_SEP
	
class FileLister:
	def __init__(self):
		allFileNameLst = [x.split(DIR_SEP)[-1] for x in glob.glob(SRC_DIR + '/*.*')]
		self.allPythonFileLst = list(filter(lambda x: '.py' in x, allFileNameLst))
		self.allTestPythonFileLst = list(filter(lambda x: 'test' in x, self.allPythonFileLst))
		self.allImageFileLst = list(filter(lambda x: '.jpg' in x, allFileNameLst))
		self.allDocFileLst = list(filter(lambda x: '.docx' in x, allFileNameLst))
		self.allReadmeFileLst = list(filter(lambda x: '.rd' in x, allFileNameLst))
	
#		print(allFileNameLst)
#		print(self.allPythonFileLst)
#		print(self.allTestPythonFileLst)
#		print(self.allImageFileLst)
#		print(self.allDocFileLst)
#		print(self.allReadmeFileLst)

	def removeTestFilesFromPythonFiles(self):
		self.allPythonFileLst = [item for item in self.allPythonFileLst if item not in self.allTestPythonFileLst]
		
if __name__ == "__main__":
	fl = FileLister()
	
	print(fl.allPythonFileLst)
	print(fl.allTestPythonFileLst)
	
	fl.removeTestFilesFromPythonFiles()
	print(fl.allPythonFileLst)
	
	