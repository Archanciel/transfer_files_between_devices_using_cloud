import os, pickle
from configobj import ConfigObj

class ConfigManager:
	"""
	This class uses ConfigObj to access to the information specified in the
	local configuration file.
	"""
	def __init__(self, configFilePathName):
		"""
		The ConfigManager constructor loads the local configuration file. Namely,
		the local dowload path, the Dropbox API key, the Dropbox base 
		application dir and the project configurations dictionary are strored
		in the ConfigManager instance variables.
		
		in order to avoid storing the Dropbox API key directly in the configuration 
		file, the key is stored in its binary form in a separate file which will
		not be uploaded to Github. The Dropbox API key was binarised using the
		storeApiKey.py utility file.
		"""
		self.config = ConfigObj(configFilePathName)

		if len(self.config) == 0:
			raise FileNotFoundError(configFilePathName + " does not exist !")

		try:
			# storing the local dowload path
			self.downloadPath = self.removeExcessiveBackslash(self.config['General']['downloadPath'])
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			# storing the Dropbox API key after reading it from its binary
			# file
			dropboxApiKeyFilePath = self.config['General']['dropboxApiKeyFilePath']
			
			with open(dropboxApiKeyFilePath, 'rb') as handle:
				dic = pickle.loads(handle.read())
				self.dropboxApiKey = dic['dropboxApiKey']
				handle.close()
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			# storing the Dropbox base dir. This base dir will contain the
			# project specific dirs
			self.dropboxBaseDir = self.config['General']['dropboxBaseDir']
		except KeyError as e:
			raise KeyError('\'' + e.args[0] + '\' parameter not defined in ' + configFilePathName)

		try:
			# storing the project configurations dictionary
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
		"""
		Returns the list of excluded dirs. Those directories will be excluded
		from searching modified files to be uploaded to the cloud.
		 
		@param projectName: project name as defined in local configuration file
		
		@return: list of full path excluded dirs
		"""
		try:
			excludedDirSectionDic = self.projects[projectName]['upload']['exclude']['directories']
		except KeyError:
			# the case if no exclude section is defined for this project in the config file
			return []

		excludedDirLst = []
		projectLocalDir = self.getProjectLocalDir(projectName)

		for exclDirKey in excludedDirSectionDic.keys():
			excludedDirLst.append(projectLocalDir + self.removeExcessiveBackslash(excludedDirSectionDic[exclDirKey]['path']))
			
		return excludedDirLst

	def getExcludedFileTypeWildchardLst(self, projectName):
		"""
		Returns the list of excluded file type for the passed project name.
		
		@param projectName: project name as defined in local configuration file
		
		@return example: ['*.pyc', '*.ini', '*.tmp']
		"""
		try:
			excludedFileTypesSectionDic = self.projects[projectName]['upload']['exclude']['filePatterns']
		except KeyError:
			# the case if no exclude section is defined for this project in the config file
			return []
			
		excludedFileTypeWildchardLst = []
		
		for wildchardFileTypeKey in excludedFileTypesSectionDic.keys():
			excludedFileTypeWildchardLst.append(excludedFileTypesSectionDic[wildchardFileTypeKey])
			
		return excludedFileTypeWildchardLst
		
	def getFilePatternLocalDestinationDic(self, projectName):
		"""
		Returns a dictionary whose keys are file wildchard patterns and values
		the corresponding directory destination project sub-dirs.
		
		@param projectName: project name as defined in local configuration file
			
		@return examplee: {'test*.py': '/test', 
							'*.py': '', 
							'*.md': '', 
							'*.docx': '/doc', 
							'*.jpg': '/images', 
							'aa*.jpg': '/images/aa'
		"""
		filePatternLocalDestinationsDic = self.projects[projectName]['download']['filePatterns']

		for key in filePatternLocalDestinationsDic.keys():
			path = filePatternLocalDestinationsDic[key]
			filePatternLocalDestinationsDic[key] = self.removeExcessiveBackslash(path)

		return filePatternLocalDestinationsDic
		
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
	print(projectSections['upload']['exclude']['directories'])
	print(cm.getExcludedDirLst(projectName))
	print(cm.getExcludedFileTypeWildchardLst(projectName))	