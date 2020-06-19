import shutil, os

from constants import *
from filelister import FileLister

class FileMover:
	def __init__(self):
		self.fileLister = FileLister()

	def moveFiles(self):		
		for fileName in self.fileLister.allTestPythonFileNameLst:
			file = DIR_SEP + fileName
			shutil.move(SRC_DIR + file, TEST_FILE_DST + file)
			print('moving {} to {}'.format(SRC_DIR + file, TEST_FILE_DST + file))

		self.fileLister.removeTestFilesFromPythonFiles()
		
		for fileName in self.fileLister.allPythonFileNameLst:
			file = DIR_SEP + fileName
			shutil.move(SRC_DIR + file, PYTHON_FILE_DST + file)
			print('moving {} to {}'.format(SRC_DIR + file, PYTHON_FILE_DST + file))
		
		for fileName in self.fileLister.allImageFileNameLst:
			file = DIR_SEP + fileName
			shutil.move(SRC_DIR + file, IMG_FILE_DST + file)
			print('moving {} to {}'.format(SRC_DIR + file, IMG_FILE_DST + file))
		
		for fileName in self.fileLister.allDocFileNameLst:
			file = DIR_SEP + fileName
			shutil.move(SRC_DIR + file, DOC_FILE_DST + file)
			print('moving {} to {}'.format(SRC_DIR + file, DOC_FILE_DST + file))
		
		for fileName in self.fileLister.allReadmeFileNameLst:
			file = DIR_SEP + fileName
			shutil.move(SRC_DIR + file, PYTHON_FILE_DST + file)
			print('moving {} to {}'.format(SRC_DIR + file, PYTHON_FILE_DST + file))

if __name__ == "__main__":
	fm = FileMover()
	fm.moveFiles()