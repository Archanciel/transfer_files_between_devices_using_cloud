from datetime import datetime

format = '%Y-%m-%d %H:%M:%S'

dateMod = datetime.strptime('2020-06-14 08:45:23', format)
print(dateMod)

format2 = '%y-%m-%d %H:%M:%S'

print(dateMod.strftime(format2))
print(datetime.now().strftime(format))

try:
	dateInval = datetime.strptime('2020-06-1408:45:23', format)
except Exception as e:
	print(e)
	
dtStr = '2020-6-4 8:5:3'
dateZeroInTime = datetime.strptime(dtStr, format)
print(dtStr, ' ', dateZeroInTime)

