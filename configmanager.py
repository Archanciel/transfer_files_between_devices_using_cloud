import os
from configobj import ConfigObj

CONFIG_SECTION_GENERAL = 'General'
CONFIG_SECTION_PROJECTS = 'Projects'

CONFIG_KEY_DOWNLOAD_PATH = 'downnloadPath'
CONFIG_KEY_DROPBOX_API_KEY = 'dropboxApiKey'
CONFIG_KEY_DROPBOX_BASE_DIR = 'dropboxBaseDir'

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
			self.dropboxBaseDir = self.config[CONFIG_SECTION_GENERAL][CONFIG_KEY_DROPBOX_BASE_DIR]
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			self.projects = self.config[CONFIG_SECTION_PROJECTS]
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' section not defined in ' + configFilePathName)

	def getProjectLocalDir(self, projectName):
		return self.projects[projectName][CONFIG_KEY_PROJECT_PATH]

	def getLastSynchTime(self, projectName):
		return self.projects[projectName][CONFIG_KEY_PROJECT_LAST_SYNC_TIME]

	def updateLastSynchTime(self, projectName, lastSynchTimeStr):
		self.projects[projectName][CONFIG_KEY_PROJECT_LAST_SYNC_TIME] = lastSynchTimeStr
		self.config.write()

	def getExcludedDirLst(self, projectName):
		excludedDirSectionLst = self.projects[projectName]['exclude']['directories']
		excludedDirLst = []
		
		for dirSection in excludedDirSectionLst:
			excludedDirLst.append(dirSection['path'])
			
		return excludedDirLst
		
	def is_section(self, config_section):
		try:
			config_section.keys()
		except AttributeError:
			return False
		else:
			return True

if __name__ == '__main__':
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'

	cm = ConfigManager(configFilePathName)
#	print("dropbox base dir ", cm.dropboxBaseDir)
#	
#	print("\nKeys in General section")
#	
#	for key in cm.config['General']: 
#		print(key)
#		
#	print("\nKeys in Project section")
#	
#	for key in cm.projects: 
#		print(key)
#		print(cm.projects[key][CONFIG_KEY_PROJECT_PATH])
#		print(cm.projects[key][CONFIG_KEY_PROJECT_LAST_SYNC_TIME])

	projectName = 'transFileCloudProject'
#	cm.updateLastSynchTime(projectName, '2020-06-22 11:45:23')
#	print("\nLast synch time ", cm.getLastSynchTime(projectName))
#	
#	print(cm.projects.keys)
	#excludedDirSectionLst = cm.projects[projectName].keys
	#print(excludedDirSectionLst)
	sections = cm.config.keys()
#	sections = cm.projects
	print(sections)
	for section in sections:
		if cm.is_section(cm.config[section]):
			for subsection in cm.config[section]:
				if cm.is_section(cm.config[section][subsection]):
					for subsection in cm.config[section][subsection]:
						print("Subsection ", subsection)		
