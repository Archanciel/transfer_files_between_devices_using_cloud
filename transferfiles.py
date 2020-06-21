import os, sys, argparse

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
			
		configManager = ConfigManager(configFilePath)
		self.downloadDir = configManager.downloadPath

		self.requester = Requester(configManager)		
		self.projectName = self.requester.getProjectName(commandLineArgs)
		self.localProjectDir = configManager.projects[self.projectName][CONFIG_KEY_PROJECT_PATH]
		self.cloudAccess = DropboxAccess(configManager, self.projectName)
		self.fileLister = FileLister(configManager=configManager, fromDir=self.downloadDir)

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
			# if the clouud directory is empty, this means
			# that we are in the state of uploading the
			# files modified on the current device to the
			# cloud so that they will be available to be
			# transfered on the other device.
			updatedFileNameLst, updatedFilePathNameLst = self.fileLister.getModifiedFileLst(self.projectName)
			questionStr = 'Those files will be uploaded to the cloud'

			if self.requester.getUserConfirmation(questionStr, updatedFileNameLst):		
				self.uploadFilesToCloud(updatedFilePathNameLst)
		else:
			# if the cloud directory contains files, this
			# means that we are in the state of transfering
			# those files to the current device. The
			# transfered files will be downloaded to the
			# download dir and deleted from the cloud.
			# They will then be moved from the download
			# dir to the correct project dir and sub dire
			localProjectDirShort = self.localProjectDir.split(DIR_SEP)[-3:]
			localProjectDirShort = DIR_SEP.join(localProjectDirShort)
			questionStr = 'Those files will be transfered from the cloud and then moved to the correct dir and sub-dir of {}'.format(localProjectDirShort)
			
			if self.requester.getUserConfirmation(questionStr, cloudFiles):
				self.transferFilesFromCloud()
			
		self.fileMover = FileMover(configManager, self.downloadDir, self.projectDir)

	def uploadFilesToCloud(self, updatedFilePathNameLst):
		#print(updatedFiles)
		pass
		
	def transferFilesFromCloud(self):
		pass
		
if __name__ == "__main__":
	tf = TransferFiles()
	print(tf.projectDir)
