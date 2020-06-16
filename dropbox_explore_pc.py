import os, dropbox

from configmanager import ConfigManager

class TransferData:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """

        with open(file_from, 'rb') as f:
            self.dbx.files_upload(f.read(), file_to)

    def download_file(self, file_from, file_to):
        with open(file_to, "wb") as f:
            metadata, res = self.dbx.files_download(path=file_from)
            f.write(res.content)
            print(metadata)
        
def main():
    if os.name == 'posix':
        CONFIG_FILE_PATH_NAME = '/sdcard/transfiles.ini'
    else:
        CONFIG_FILE_PATH_NAME = 'c:\\temp\\transfiles.ini'

    cm = ConfigManager(CONFIG_FILE_PATH_NAME)
    access_token = cm.dropboxApiKey
    transferData = TransferData(access_token)

    file_from = 'filemover.py'
    file_to = '/test_dropbox/filemover.py'  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

    file_from = '/test_dropbox/filemover.py' # The full path of the file to download, including the file name
    file_to = 'filemover_downloaded.py'
    transferData.download_file(file_from, file_to)
    

if __name__ == '__main__':
    main()
