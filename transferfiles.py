from datetime import datetime

from constants import *
from requester import Requester
from configmanager import * 
from filelister import FileLister
from filemover import FileMover
from dropboxaccess import DropboxAccess

class TransferFiles:
	def __init__(self, configFilePath=None, commandLineArgs=None):
		"""
		    :param configFilePath used for unit testing only
		    :param commandLineArgs: used for unit testing only
		"""
		if configFilePath == None:
			# we are not unit testing ...
			configFilePath = CONFIG_FILE_PATH_NAME
			
		self.configManager = ConfigManager(configFilePath)
		self.downloadDir = self.configManager.downloadPath

		self.requester = Requester(self.configManager)
		self.projectName = self.requester.getProjectName(commandLineArgs)
		self.localProjectDir = self.configManager.getProjectLocalDir(self.projectName)
		self.cloudAccess = DropboxAccess(self.configManager, self.projectName)
		self.fileLister = FileLister(configManager=self.configManager, fromDir=self.downloadDir)

		cloudFiles = []
		
		try:
			cloudFiles = self.cloudAccess.getCloudFileList()
		except NotADirectoryError as e:
			# means that the cloud project directory does not exist
			#print(str(e))
			questionStr = 'Cloud project directory {} does not exist and will be created'.format(self.projectName)

			if self.requester.getUserConfirmation(questionStr):		
				self.cloudAccess.createProjectFolder()

		if cloudFiles == []:
			# if the clouud directory is empty, this means# that we are in the state of uploading the
			# files modified on the current device to the cloud so that they will be available to be
			# transferred on the other device.
			self.handleUploadState()
		else:
			# if the cloud directory contains files, this means that we are in the state of transferring
			# those files to the current device. The transferred files will be downloaded to the
			# download dir and deleted from the cloud. They will then be moved from the download
			# dir to the correct project dir and sub dirs
			localProjectDirShort = self.localProjectDir.split(DIR_SEP)[-3:]
			localProjectDirShort = DIR_SEP.join(localProjectDirShort)
			questionStr = 'Those files will be transferred from the cloud and then moved to the correct dir and sub-dir of {}'.format(localProjectDirShort)
			
			if self.requester.getUserConfirmation(questionStr, cloudFiles):
				print('')  # empty line
				self.transferFilesFromCloud()
				print('')  # empty line

				# moving file from dowload dir to project dest dir and sub-dirs
				fileMover = FileMover(self.configManager, self.downloadDir, self.localProjectDir)
				fileMover.moveFiles()
			else:
				# list modified local files and ask if they should be uploaded. Handles the
				# case where you did an upload and then modified files again on the same
				# device and want to add those files to the cloud
				self.handleUploadState()

	def handleUploadState(self):
		updatedFileNameLst, updatedFilePathNameLst, lastSyncTimeStr = self.fileLister.getModifiedFileLst(self.projectName)
		questionStr = 'Those files were modified locally after {} and will be uploaded to the cloud'.format(lastSyncTimeStr)

		if self.requester.getUserConfirmation(questionStr, updatedFileNameLst):
			print('')  # empty line
			self.uploadFilesToCloud(updatedFilePathNameLst)

	def uploadFilesToCloud(self, updatedFilePathNameLst):
		for localFilePathName in updatedFilePathNameLst:
			print('Uploading {} to the cloud ...'.format(localFilePathName.split(DIR_SEP)[-1]))
			self.cloudAccess.uploadFile(localFilePathName)

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

	def updateLastSynchTime(self):
		lastSynchTimeStr = datetime.now().strftime(DATE_TIME_FORMAT)
		self.configManager.updateLastSynchTime(self.projectName, lastSynchTimeStr)
		print('\nUpdated last synch time to ' + lastSynchTimeStr)

	def transferFilesFromCloud(self):
		cloudFileNameLst = self.cloudAccess.getCloudFileList()

		for fileName in cloudFileNameLst:
			destFileName = self.configManager.downloadPath + DIR_SEP + fileName
			print('Transferring {} from the cloud ...'.format(fileName))
			self.cloudAccess.downloadFile(fileName, destFileName)
			self.cloudAccess.deleteFile(fileName)

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

if __name__ == "__main__":
	tf = TransferFiles()
