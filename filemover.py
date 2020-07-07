import shutil, os

from constants import *
from configmanager import ConfigManager
from filelister import FileLister

class FileMover:
	def __init__(self, configManager, downloadDir, localProjectDir):
		self.fileNameLister = FileLister(configManager, downloadDir)
		self.downloadDir = downloadDir
		self.projectDir = localProjectDir

	def moveFiles(self):		
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

if __name__ == "__main__":
	fromDir = '/storage/emulated/0/Download'
	projectDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/'

	fm = FileMover(ConfigManager('/sdcard/transfiles.ini'), fromDir, projectDir)
	fm.moveFiles()