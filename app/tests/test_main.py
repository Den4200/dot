import shlex

with open('app\\tests\\test.do', 'r') as f:
    print(shlex.split(f.read(), posix=False))
