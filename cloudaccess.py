from abc import ABCMeta
from abc import abstractmethod

class CloudAccess(metaclass=ABCMeta):
	def __init__(self, cloudTransferBaseDir, projectName):
		self.cloudTransferDir = cloudTransferBaseDir + '/' + projectName
	@abstractmethod	
	def uploadFiles(self):
		pass
		
	@abstractmethod	
	def downloadFiles(self):
		pass

	@abstractmethod
	def deleteFiles(self, file):
		pass

	@abstractmethod
	def getCloudFileList(self):
		pass
