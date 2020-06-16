from cloudaccess import CloudAccess
from configmanager import ConfigManager

class DropboxAccess(CloudAccess):
	def __init__(self, configManager):
		super().__init__()
		accessToken = configManager.dropboxApiKey
			
	def uploadFiles(self):
		pass
			
	def downloadFiles(self):
		pass