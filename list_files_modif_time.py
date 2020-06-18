import os
import datetime

format = '%Y-%m-%d %H:%M:%S'

query_date = datetime.datetime.strptime('2020-06-18 09:45:23', format)

#query_date = datetime.datetime.fromtimestamp(int(float(1516188526532974000)/1000000000))
fromDir = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/trans_file_cloud'
results = []

for root, dirs, files in os.walk(fromDir):
    for filename in files:
        path = os.path.join(root, filename)
        file_mtime = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
        if(file_mtime > query_date):
            results.append(path)  # yield path?

print(results)