import os
from configobj import ConfigObj

CONFIG_SECTION_GENERAL = 'General'
CONFIG_SECTION_PROJECTS = 'Projects'

CONFIG_KEY_DOWNLOAD_PATH = 'downnloadPath'
CONFIG_KEY_DROPBOX_API_KEY = 'dropboxApiKey'

#CONFIG_KEY_TRANS_FILE_CLOUD_TEST_PROJECT = 'transFileCloudTestProjectPath'
CONFIG_KEY_PROJECT_PATH = 'projectPath'
CONFIG_KEY_PROJECT_LAST_SYNC_TIME = 'lastSyncTime'

class ConfigManager:
	def __init__(self, configFilePathName):
		self.config = ConfigObj(configFilePathName)

		if len(self.config) == 0:
			raise FileNotFoundError(configFilePathName + " does not exist !")

		try:
			self.downloadPath = self.config[CONFIG_SECTION_GENERAL][CONFIG_KEY_DOWNLOAD_PATH]
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			self.dropboxApiKey = self.config[CONFIG_SECTION_GENERAL][CONFIG_KEY_DROPBOX_API_KEY]
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			self.projects = self.config[CONFIG_SECTION_PROJECTS]
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' section not defined in ' + configFilePathName)

if __name__ == '__main__':
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'

	cm = ConfigManager(configFilePathName)
	#print(cm.downloadPath)
	#print(cm.dropboxApiKey)

	#print(cm.config[CONFIG_SECTION_PROJECTS]['transFileCloudTestProject'])
	
	for key in cm.projects: 
		print(key)
		print(cm.projects[key][CONFIG_KEY_PROJECT_PATH])
		print(cm.projects[key][CONFIG_KEY_PROJECT_LAST_SYNC_TIME])
