from abc import ABCMeta
from abc import abstractmethod

class CloudAccess(metaclass=ABCMeta):
	def __init__(self):
		pass
		
	@abstractmethod	
	def uploadFiles(self):
		pass
		
	@abstractmethod	
	def downloadFiles(self):
		pass

	@abstractmethod
	def deleteFiles(self, file):
		pass
