import os, pickle
from configobj import ConfigObj

class ConfigManager:
	def __init__(self, configFilePathName):
		self.config = ConfigObj(configFilePathName)

		if len(self.config) == 0:
			raise FileNotFoundError(configFilePathName + " does not exist !")

		try:
			self.downloadPath = self.removeExcessiveBackslash(self.config['General']['downloadPath'])
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			dropboxApiKeyFilePath = self.config['General']['dropboxApiKeyFilePath']
			
			with open(dropboxApiKeyFilePath, 'rb') as handle:
				dic = pickle.loads(handle.read())
				self.dropboxApiKey = dic['dropboxApiKey']
				handle.close()
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			self.dropboxBaseDir = self.config['General']['dropboxBaseDir']
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			self.projects = self.config['Projects']
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' section not defined in ' + configFilePathName)

	def removeExcessiveBackslash(self, path):
		"""
		In the config ini files on Windows, the paths are specified using double
		backslash dir separators. This is done to avoid a problem which would
		appear in case a sub dir name starts withsminus t, like in c:\temp. In 
		such a case, \t is interpreted like a TAB character, which results to
		c:	temp !! So, c:\temp is specified as c.\\temp in the ini file.
		
		But when configobj reads in a path specified with double backslash,
		it return four backslashes as dir separators. o:\\temp is returned 
		as c:\\\\temp. This can cause problems, like in FileLister in which
		os.walk() returns double backslashes for dir separators.
		
		This method removes the excessive backslashes when needed.
		
		@param path path with maybe \\\\ as dir separators
		
		@return path with \\ dir separators
		"""
		return path.replace('\\\\', '\\')

	def getProjectLocalDir(self, projectName):
		return self.removeExcessiveBackslash(self.projects[projectName]['projectPath'])

	def getLastSynchTime(self, projectName):
		return self.projects[projectName]['lastSyncTime']

	def updateLastSynchTime(self, projectName, lastSynchTimeStr):
		self.projects[projectName]['lastSyncTime'] = lastSynchTimeStr
		self.config.write()

	def getExcludedDirLst(self, projectName):
		try:
			excludedDirSectionLst = self.projects[projectName]['upload']['exclude']['directories']
		except KeyError:
			# the case if no exclude section is defined for this project in the config file
			return []

		excludedDirLst = []
		
		for dirSection in excludedDirSectionLst:
			excludedDirLst.append(self.getProjectLocalDir(projectName) + self.removeExcessiveBackslash(excludedDirSectionLst[dirSection]['path']))
			
		return excludedDirLst

	def getExcludedFileTypeWildchardLst(self, projectName):
		try:
			excludedFileTypesSection = self.projects[projectName]['upload']['exclude']['filePatterns']
		except KeyError:
			# the case if no exclude section is defined for this project in the config file
			return []
			
		excludedFileTypeWildchardLst = []
		
		for wildchardFileType in excludedFileTypesSection:
			excludedFileTypeWildchardLst.append(excludedFileTypesSection[wildchardFileType])
			
		return excludedFileTypeWildchardLst
		
if __name__ == '__main__':
	if os.name == 'posix':
		configFilePathName = '/sdcard/transfiles.ini'
	else:
		configFilePathName = 'c:\\temp\\transfiles.ini'

	cm = ConfigManager(configFilePathName)

	if os.name == 'posix':
		configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud/test/transfiles.ini'
	else:
		configFilePathName = 'D:\\Development\\Python\\trans_file_cloud\\test\\transfiles.ini'
		
	cm = ConfigManager(configFilePathName)		
	projectName = 'transFileCloudProject'
		
	projectSections = cm.projects[projectName]
	print('first trial')
	print(projectSections)
	
#	def is_section(config_section):
#		try:
#			config_section.keys()
#		except AttributeError:
#			return False
#		else:
#			return True
#		
#	for section in projectSections:
#		if is_section(projectSections[section]):
#			for subsection in projectSections[section]:
#				if is_section(projectSections[section][subsection]):
#					for subsection in projectSections[section][subsection]:
#						print("Subsection ", subsection)
						
#	print('\nNew trial')		

#	def gather_subsection(section, key):
#		if section.depth > 1:
#			print("Subsection " + section.name)

#	cm.projects[projectName].walk(gather_subsection)

	print(projectSections['upload']['exclude']['directories'])
	print(cm.getExcludedDirLst(projectName))
	print(cm.getExcludedFileTypeWildchardLst(projectName))	