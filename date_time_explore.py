from datetime import datetime

format = '%Y-%m-%d %H:%M:%S'

dateMod = datetime.strptime('2020-06-14 08:45:23', format)
print(dateMod)

format2 = '%y-%m-%d %H:%M:%S'

print(dateMod.strftime(format2))
print(datetime.now().strftime(format))

dateInval = datetime.strptime('2020-06-1408:45:23', format)
