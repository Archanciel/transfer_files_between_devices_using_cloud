import re

pattern = re.compile('[\w:\./]*\.[py]*$')
l1 = ['/dir/ru.ff/trans_proj_dir/file2.txt', "/dir/ru.ff/trans_proj_dir/file.py"]
l2 = [ s for s in l1 if pattern.match(s) ]
print(l1)
print(l2)