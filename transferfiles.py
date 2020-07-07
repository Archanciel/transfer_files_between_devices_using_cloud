from datetime import datetime

from constants import *
from requester import Requester
from configmanager import * 
from filelister import FileLister
from filemover import FileMover
from dropboxaccess import DropboxAccess

class TransferFiles:
	def __init__(self, configFilePath=None, projectName=None):
		"""
		    @param configFilePath: used for unit testing only
		    @param projectName used for unit testing only
		"""
		if configFilePath == None:
			# we are not unit testing ...
			configFilePath = CONFIG_FILE_PATH_NAME
			
		self.configManager = ConfigManager(configFilePath)
		self.requester = Requester(self.configManager)
			
		if projectName == None:
			# we are not unit testing ...
			projectName = self.requester.getProjectName()
		
			if projectName == None:
				# user did choose Quit
				self.projectName = None
				return
			
		self.projectName = projectName
		self.downloadDir = self.configManager.downloadPath
		self.localProjectDir = self.configManager.getProjectLocalDir(self.projectName)
		self.cloudAccess = DropboxAccess(self.configManager, self.projectName)
		self.fileLister = FileLister(configManager=self.configManager, downloadDir=self.downloadDir)

	def transferFiles(self, commandLineArgs=None):
		"""

		@param commandLineArgs: used for unit testing only
		"""
		if self.projectName == None:
			# user did choose Quit
			return
			
		cloudFileLst = []

		try:
			cloudFileLst = self.cloudAccess.getCloudFileList()
		except NotADirectoryError as e:
			# means that the cloud project directory does not exist
			if self.requester.getCreateCloudFolderConfirmation(self.projectName):
				self.cloudAccess.createProjectFolder()
			else:
				return 

		if cloudFileLst == []:
			# if the cloud directory is empty, this means that we are in the state of uploading
			# to the cloud the files modified on the current device so that they will be available
			# to be transferred from the cloud to the local directories on the other device.
			self.uploadModifiedFilesToCloud()
		else:
			# if the cloud directory contains files, this means that we are in the state of transferring
			# those files to the current device. The transferred files will be downloaded to the
			# local download dir and deleted from the cloud. They will then be moved from the download
			# dir to the correct project dir and sub dirs.
			self.transferFilesFromCloudToLocalDirs(cloudFileLst)

	def transferFilesFromCloudToLocalDirs(self, cloudFileLst):
		"""

		@param cloudFileLst:
		"""
		localProjectDirShort = DIR_SEP.join(self.localProjectDir.split(DIR_SEP)[-3:])

		questionStr = 'vvv {} files will be transferred from the cloud and then moved to the correct dir and sub-dir of {}.\nIf you want to upload new modified files instead, type N'.format(
			len(cloudFileLst), localProjectDirShort)
		doDownload, _ = self.requester.getUserConfirmation(questionStr, cloudFileLst)

		if doDownload:
			print('')  # empty line
			self.transferFilesFromCloud()
			print('')  # empty line

			# moving file from dowload dir to project dest dir and sub-dirs
			fileMover = FileMover(self.configManager, self.downloadDir, self.localProjectDir)
			fileMover.moveFiles()

			# updating last synch time for the project in config file
			self.updateLastSynchTime()
		else:
			# list modified local files and ask if they should be uploaded. Handles the
			# case where you did an upload and then modified files again on the same
			# device and want to add those files to the cloud
			self.uploadModifiedFilesToCloud()

	def uploadModifiedFilesToCloud(self):
		"""

		"""
		updatedFileNameLst, updatedFilePathNameLst, lastSyncTimeStr = self.fileLister.getModifiedFileLst(self.projectName)
		
		if updatedFileNameLst == []:
			print('\nNo files modified locally since last sync time {}'.format(lastSyncTimeStr))
		else:
			questionStr = '^^^ {} files were modified locally after {}\nand will be uploaded to the cloud.\nChoose P to display the path and U to update the last sync time'.format(
				len(updatedFileNameLst), lastSyncTimeStr)
			doUpload, lastSynchTimeChoice = self.requester.getUserConfirmation(questionStr, updatedFileNameLst, updatedFilePathNameLst)

			if doUpload: 
				print('')  # empty line
				self.uploadToCloud(updatedFilePathNameLst)
			elif lastSynchTimeChoice == '':
				# the user did choose not to upload anything and to leave the last sync
				# time unchanged
				return
			elif lastSynchTimeChoice == 'N':
				# the user did choose to update the last sync time to current time (now)
				self.updateLastSynchTime()
			else:
				# the user did enter a last sync time manually
				self.updateLastSynchTime(lastSynchTimeChoice)

	def uploadToCloud(self, updatedFilePathNameLst):
		"""

		@param updatedFilePathNameLst:
		"""
		for localFilePathName in updatedFilePathNameLst:
			print('Uploading {} to the cloud ...'.format(localFilePathName.split(DIR_SEP)[-1]))
			self.cloudAccess.uploadFile(localFilePathName)

		# updating last synch time for the project in config file
		self.updateLastSynchTime()

	def updateLastSynchTime(self, lastSynchTimeStr=''):
		"""

		"""
		if lastSynchTimeStr == '':
			lastSynchTimeStr = datetime.now().strftime(DATE_TIME_FORMAT)
		elif not self.validateLastSynchTimeStr(lastSynchTimeStr):
			print('\nSynch time format invalid {}. Nothing changed.'.format(lastSynchTimeStr))

			return
		
		self.configManager.updateLastSynchTime(self.projectName, lastSynchTimeStr)
		print('\nUpdated last synch time to ' + lastSynchTimeStr)

	def validateLastSynchTimeStr(self, lastSynchTimeStr):
		try:
			datetime.strptime(lastSynchTimeStr, DATE_TIME_FORMAT)
			return True
		except ValueError:
			return False
		
	def transferFilesFromCloud(self):
		"""

		"""
		cloudFileNameLst = self.cloudAccess.getCloudFileList()

		for fileName in cloudFileNameLst:
			destFileName = self.configManager.downloadPath + DIR_SEP + fileName
			print('Transferring {} from the cloud ...'.format(fileName))
			self.cloudAccess.downloadFile(fileName, destFileName)
			self.cloudAccess.deleteFile(fileName)

if __name__ == "__main__":
	tf = TransferFiles()
	tf.transferFiles()
