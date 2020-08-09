from abc import ABCMeta
from abc import abstractmethod

from constants import DIR_SEP

class CloudAccess(metaclass=ABCMeta):
	def __init__(self, cloudTransferBaseDir, projectName):
		"""
		CloudAccess constructor. Initialises the project cloud directory
		path name using information obtained by the CloudAccess subclass
		from the configuration manager.
		
		@param cloudTransferBaseDir: information defined in the local 
									 configuration file
		@param projectName: name of the project for which the CloudAccess
							class is initialized
		@param localProjectDir: local project dir used when handling path
								component of uploaded or downloaded files
		"""
		self.cloudProjectDir = cloudTransferBaseDir + '/' + projectName

	@abstractmethod	
	def uploadFileName(self, localFilePathName):
		pass

	@abstractmethod
	def uploadFilePathName(self, localFilePathName, localProjectDir):
		pass

	@abstractmethod	
	def downloadFile(self):
		pass

	@abstractmethod
	def deleteFile(self, file):
		pass

	@abstractmethod
	def deleteProjectSubFolder(self, subFolderName):
		pass

	@abstractmethod
	def deleteProjectFolder(self):
		pass

	@abstractmethod
	def getCloudFileNameList(self):
		pass

	@abstractmethod
	def getCloudFilePathNameList(self):
		pass

	@abstractmethod
	def createProjectSubFolder(self, subFolderName):
		pass
