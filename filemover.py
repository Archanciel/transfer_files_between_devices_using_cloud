import shutil, os

from constants import *
from configmanager import ConfigManager
from filelister import FileLister

class FileMover:
	def __init__(self, configManager, projectName):
		"""
		@param configManager:
		@param projectName:
		"""
		self.projectName = projectName
		self.downloadDir = configManager.downloadPath
		self.projectDir = configManager.getProjectLocalDir(projectName)
		self.fileNameLister = FileLister(configManager)

	def moveFilesToDel(self):		
		for fileName in self.fileNameLister.allTestPythonFileNameLst:
			fromFilePath = self.downloadDir + DIR_SEP + fileName
			toFilePath = self.projectDir + TEST_SUB_DIR + DIR_SEP + fileName
			shutil.move(fromFilePath, toFilePath)
			print('moving {} to {}'.format(fromFilePath.replace(BASE_DST_FILE_DIR, ''), toFilePath.replace(BASE_DST_FILE_DIR, '')))

		self.fileNameLister.removeTestFilesFromPythonFilesLst()
		
		for fileName in self.fileNameLister.allPythonFileNameLst:
			fromFilePath = self.downloadDir + DIR_SEP + fileName
			toFilePath = self.projectDir + DIR_SEP + fileName
			shutil.move(fromFilePath, toFilePath)
			print('moving {} to {}'.format(fromFilePath.replace(BASE_DST_FILE_DIR, ''), toFilePath.replace(BASE_DST_FILE_DIR, '')))
		
		for fileName in self.fileNameLister.allImageFileNameLst:
			fromFilePath = self.downloadDir + DIR_SEP + fileName
			toFilePath = self.projectDir + IMG_SUB_DIR + DIR_SEP + fileName
			shutil.move(fromFilePath, toFilePath)
			print('moving {} to {}'.format(fromFilePath.replace(BASE_DST_FILE_DIR, ''), toFilePath.replace(BASE_DST_FILE_DIR, '')))
		
		for fileName in self.fileNameLister.allDocFileNameLst:
			fromFilePath = self.downloadDir + DIR_SEP + fileName
			toFilePath = self.projectDir + DOC_SUB_DIR + DIR_SEP + fileName
			shutil.move(fromFilePath, toFilePath)
			print('moving {} to {}'.format(fromFilePath.replace(BASE_DST_FILE_DIR, ''), toFilePath.replace(BASE_DST_FILE_DIR, '')))
		
		for fileName in self.fileNameLister.allReadmeFileNameLst:
			fromFilePath = self.downloadDir + DIR_SEP + fileName
			toFilePath = self.projectDir + DIR_SEP + fileName
			shutil.move(fromFilePath, toFilePath)
			print('moving {} to {}'.format(fromFilePath.replace(BASE_DST_FILE_DIR, ''), toFilePath.replace(BASE_DST_FILE_DIR, '')))

	def moveFiles(self):
		"""
			orderedFileTypeWildchardExprLst and fileTypeDic examples:
				
			['test*.py', 'aa*.jpg', '*.jpg', '*.docx', '*.py', '*.rd'], orderedFileTypeWildchardExprLst)

			{'*.jpg': ('/images', ['current_state_21.jpg', 'current_state_22.jpg']), 
			'*.docx': ('/doc', ['doc_21.docx', 'doc_22.docx']),
			'*.rd': ('/', ['README_2.rd']),
			'aa*.jpg': ('/images/aa', ['aa_current.jpg']),
			'test*.py': ('/test', ['testfilelister_2.py', 'testfilemover_2.py']),
			'*.py': ('/', ['constants_2.py', 'filelister_2.py', 'filemover_2.py'])}, fileTypeDic)
		"""
		orderedFileTypeWildchardExprLst, fileTypeDic = self.fileNameLister.getFilesByOrderedTypes(self.projectName, self.downloadDir)
		
		for fileTypeWildchardExpr in orderedFileTypeWildchardExprLst:
			fileTypeEntryTuple = fileTypeDic[fileTypeWildchardExpr]
			destinationDir = self.projectDir + fileTypeEntryTuple[0]
			fileToMoveNameLst = fileTypeEntryTuple[1]
			for fileToMoveName in fileToMoveNameLst:
				fromFilePath = self.downloadDir + DIR_SEP + fileToMoveName
				toFilePath = destinationDir + DIR_SEP + fileToMoveName
				shutil.move(fromFilePath, toFilePath)
				
				fromFilePathShortened = self.shortenFileNamePath(fromFilePath)
				toFilePathShortened = self.shortenFileNamePath(toFilePath)
				print('moving {} to {}'.format(fromFilePathShortened, toFilePathShortened))

	def shortenFileNamePath(self, completeFilePathName):
		"""
		here, the completeFilePathName is a fuLl file path name. In order
		to display a more readable file list, only the last 4 file
		pathName elements are kept.
		"""
		filePathNameElementLst = completeFilePathName.split(DIR_SEP)
		
		return DIR_SEP.join(filePathNameElementLst[-4:])
									
		
if __name__ == "__main__":
	fromDir = '/storage/emulated/0/Download'
	projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/'

	fm = FileMover(ConfigManager('/sdcard/transfiles.ini'), fromDir, projectDir)
	fm.moveFiles()