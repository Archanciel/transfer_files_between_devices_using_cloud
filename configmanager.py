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

	if os.name == 'posix':
		configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
	else:
		configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
	cm = ConfigManager(configFilePathName)		
	projectName = 'transFileCloudProject'
		
	projectSections = cm.projects[projectName]
	print('first trial')
	print(projectSections)
		
#	for section in projectSections:
#		if cm.is_section(projectSections[section]):
#			for subsection in projectSections[section]:
#				if cm.is_section(projectSections[section][subsection]):
#					for subsection in projectSections[section][subsection]:
#						print("Subsection ", subsection)
						
#	print('\nNew trial')		

#	def gather_subsection(section, key):
#		if section.depth > 1:
#			print("Subsection " + section.name)

#	cm.projects[projectName].walk(gather_subsection)

	print(projectSections['exclude']['directories'])
	print(cm.getExcludedDirLst(projectName))