import shutil, os

from constants import *
from configmanager import ConfigManager
from filelister import FileLister

class FileMover:
	"""
	This class manages the physical moving of the files from the local
	download dir to the correct target dirs which depend on the file type or
	name pattern as defined in the local configuration file.
	"""
	def __init__(self, configManager, projectName):
		"""
		FileMover constructor.
		
		@param configManager: ConfigManager giving access to the local configuration
							  file data
		@param projectName: project name as defined in the local configuration
							file
		"""
		self.projectName = projectName
		self.downloadDir = configManager.downloadPath
		self.projectDir = configManager.getProjectLocalDir(projectName)
		self.fileNameLister = FileLister(configManager)

	def moveFiles(self):
		"""
		This method performs the physical moving of the files from the local
		download dir to the correct target dirs which depend on the file type or
		name pattern as defined in the local configuration file.
		
		It uses a FileLister instance to obtain the required information for 
		transfering the files at their right destination.
		
		Here are an example of the two data structures returned by FileLister 
		and used by FileMover to transfer files in the adequate order at their 
		local destination:
			
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
		This method shortens the full path file name string to make it more
		readable by the user. Here, the completeFilePathName is a fuLl file path
		name. In order to display a more readable file list, only the last 4 file
		pathName elements are kept.
		
		@param completeFilePathName: fuLl file path name
		"""
		filePathNameElementLst = completeFilePathName.split(DIR_SEP)
		
		return DIR_SEP.join(filePathNameElementLst[-4:])									
		
if __name__ == "__main__":
	fromDir = '/storage/emulated/0/Download'
	projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/'

	fm = FileMover(ConfigManager('/sdcard/transfiles.ini'), fromDir, projectDir)
	fm.moveFiles()