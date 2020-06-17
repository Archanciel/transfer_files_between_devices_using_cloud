import os, sys, argparse

from constants import *
from requester import Requester
from configmanager import ConfigManager 
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
		requester = Requester(configManager)
		
		requester.getProjectName(commandLineArgs)
		
		downLoadDir = configManager.downloadPath
		self.fileLister = FileLister(configManager=configManager, fromDir=downLoadDir)
		projectDir = configManager.projects['transFileCloudTestProject']['projectPath']
		self.fileMover = FileMover(configManager, downLoadDir, projectDir)
		self.cloudAccess = DropboxAccess(configManager)

if __name__ == "__main__":
	tf = TransferFiles()