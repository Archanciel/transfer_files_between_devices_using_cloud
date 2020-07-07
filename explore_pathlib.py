from pathlib import Path
root = Path('D:\\Development\\Python\\trans_file_cloud\\.git')
child = Path('D:\\Development\\Python\\trans_file_cloud\\.git\\hooks')
other = Path('/some/other/path')


print(root in child.parents)